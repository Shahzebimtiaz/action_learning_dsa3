import requests
import psycopg2

# Define the base URL for FHIR API
BASE_URL = 'https://hapi.fhir.org/baseR4'

def fetch_observations():
    url = f"{BASE_URL}/Observation"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def process_data(fhir_data):
    notes = []
    for entry in fhir_data.get('entry', []):
        resource = entry.get('resource', {})
        if resource.get('resourceType') == 'Observation':
            # Extract note_type
            note_type = resource.get('code', {}).get('text', 'unknown_type')
            
            # Extract display field from the first component's code
            display_text = "unknown_display"
            if resource.get('component'):
                for component in resource['component']:
                    coding = component.get('code', {}).get('coding', [])
                    if coding:
                        display_text = coding[0].get('display', 'unknown_display')
                        break  # Use the first available display text
            
            # Extract NCT ID (or other identifier, if applicable)
            nct_id = resource.get('code', {}).get('coding', [{}])[0].get('code', 'unknown_code')
            
            # Format note_text
            note_text = f"{display_text} ({note_type})"

            # Append the note
            notes.append((nct_id, note_type, note_text))
    return notes

def insert_clinical_notes(notes):
    conn = psycopg2.connect(
        dbname='clinicalbert_app',
        user='clinicalbert_user',
        password='password',
        host='localhost'
    )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO clinical_notes (nct_id, note_type, note_text)
    VALUES (%s, %s, %s)
    ON CONFLICT (nct_id) DO NOTHING;
    """

    cursor.executemany(insert_query, notes)
    conn.commit()
    cursor.close()
    conn.close()

def main():
    try:
        # Fetch data from FHIR server
        fhir_data = fetch_observations()
        
        # Process the data
        notes = process_data(fhir_data)
        
        # Store the data in PostgreSQL
        insert_clinical_notes(notes)
        
        print("Data integration completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
