import streamlit as st
import requests
import pandas as pd
import json

def fetch_ner_entities(text):
    try:
        response = requests.post("http://localhost:8000/api/v1/endpoints/ner/", json={"text": text})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching NER data: {e}")
        return {}

def combine_tokens(tokens, labels):
    entities = []
    current_entity = {"text": "", "label": ""}
    
    for token, label in zip(tokens, labels):
        if label.startswith("B-"):
            if current_entity["text"]:
                entities.append(current_entity)
            current_entity = {"text": token, "label": label[2:]}
        elif label.startswith("I-"):
            if current_entity["label"] == label[2:]:
                current_entity["text"] += token
            else:
                if current_entity["text"]:
                    entities.append(current_entity)
                current_entity = {"text": token, "label": label[2:]}
        else:
            if current_entity["text"]:
                entities.append(current_entity)
            current_entity = {"text": token, "label": "O"}
    
    if current_entity["text"]:
        entities.append(current_entity)
    
    return entities

def main():
    st.title("Entity Detail Page")

    input_text = st.text_area("Enter clinical text for analysis:", "")

    if st.button("Analyze Text"):
        if input_text:
            data = fetch_ner_entities(input_text)
            tokens = data.get("tokens", [])
            labels = data.get("labels", [])
            entities = combine_tokens(tokens, labels)
            
            # Display entities with highlighted text
            st.write("## Recognized Entities")
            for entity in entities:
                if entity["label"] != "O":
                    st.write(f"- {entity['text']} ({entity['label']})")
            
            # Display recommendations if available
            st.write("## Recommendations")
            recommendations = data.get("recommendations", [])
            if recommendations:
                for rec in recommendations:
                    st.write(f"- {rec}")
            else:
                st.write("No recommendations available.")
            
            # Download options for processed data
            if st.button("Download Recognized Entities as CSV"):
                df_entities = pd.DataFrame(entities)
                csv_data = df_entities.to_csv(index=False)
                st.download_button("Download CSV", csv_data, file_name="recognized_entities.csv", mime="text/csv")

            if st.button("Download Recommendations as JSON"):
                json_data = json.dumps({"recommendations": recommendations}, indent=4)
                st.download_button("Download JSON", json_data, file_name="recommendations.json", mime="application/json")
        else:
            st.warning("Please enter some text for analysis.")

if __name__ == "__main__":
    main()
