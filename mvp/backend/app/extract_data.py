import csv
import os
import psycopg2

def fetch_notes_from_db():
    conn = psycopg2.connect(
        dbname='clinicalbert_app',
        user='clinicalbert_user',
        password='password',
        host='localhost'
    )
    cursor = conn.cursor()
    
    select_query = "SELECT nct_id, note_type, note_text FROM clinical_notes"
    cursor.execute(select_query)
    notes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return notes

def save_to_csv(notes, filename='clinical_notes.csv'):
    # Ensure the directory exists
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['nct_id', 'note_type', 'note_text'])  # Write header
        writer.writerows(notes)

def main():
    try:
        # Fetch notes from PostgreSQL database
        notes = fetch_notes_from_db()
        
        # Save the data to a CSV file
        save_to_csv(notes, '../data_raw/clinical_notes.csv')
        
        print("Data exported to CSV successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
