import spacy
import json
import logging
import re
from pathlib import Path

# Configure logging
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(filename='logs/ner_analysis.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

def perform_ner(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_, ent.start_char, ent.end_char) for ent in doc.ents]
    return entities

def categorize_entities(entities):
    categories = {
        "Name": [],
        "Rank": [],
        "Address": [],
        "PhoneNo": [],
        "Pin": [],
        "ID": [],
        "Location": [],
        "MainEventsInvolvedIn": [],
        "Date": [],
        "Organization": [],
    }
    
    rank_patterns = r'\b(Private|Corporal|Sergeant|Lieutenant|Captain|Major|Colonel|General)\b'
    
    for text, label, _, _ in entities:
        if label == "PERSON":
            categories["Name"].append(text)
        elif label in ["GPE", "LOC"]:
            categories["Location"].append(text)
        elif re.match(r'\d{5,}', text):
            categories["Pin"].append(text)
            categories["ID"].append(text)
        elif re.match(r'\d{3}[-\.\s]?\d{3}[-\.\s]?\d{4}', text):
            categories["PhoneNo"].append(text)
        elif label == "EVENT":
            categories["MainEventsInvolvedIn"].append(text)
        elif label == "DATE":
            categories["Date"].append(text)
        elif label == "ORG":
            categories["Organization"].append(text)
        elif re.match(rank_patterns, text, re.IGNORECASE):
            categories["Rank"].append(text)
        
        # Address detection (simple heuristic)
        if any(word in text.lower() for word in ['street', 'avenue', 'road', 'lane']):
            categories["Address"].append(text)
    
    return categories

def generate_summary(categories):
    summary = []
    events = categories["MainEventsInvolvedIn"]
    dates = categories["Date"]
    organizations = categories["Organization"]
    
    # Combine all unique information
    all_info = set()
    for name in categories["Name"]:
        rank = categories["Rank"][0] if categories["Rank"] else ""
        org = organizations[0] if organizations else "an unknown organization"
        event = events[0] if events else "an unspecified event"
        date = dates[0] if dates else "an unknown date"
        
        info = f"{rank + ' ' if rank else ''}{name} from {org} was involved in {event} on {date}."
        all_info.add(info)
    
    # Create a coherent summary
    if all_info:
        summary.append("Summary of identified individuals and their activities:")
        for info in all_info:
            summary.append("- " + info)
        
        # Add additional information if available
        if len(organizations) > 1:
            summary.append(f"\nOther organizations mentioned: {', '.join(organizations[1:])}")
        if len(events) > 1:
            summary.append(f"\nOther events mentioned: {', '.join(events[1:])}")
        if len(dates) > 1:
            summary.append(f"\nOther dates mentioned: {', '.join(dates[1:])}")
    else:
        summary.append("No specific individuals or activities were identified in the text.")
    
    return "\n".join(summary)

def save_results(categories, file_path):
    Path("results").mkdir(exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(categories, f, indent=2)

def perform_ner_with_logging(text):
    logging.info("Starting NER analysis")
    entities = perform_ner(text)
    logging.info(f"Detected entities: {entities}")
    categories = categorize_entities(entities)
    logging.info(f"Categorized entities: {categories}")
    summary = generate_summary(categories)
    logging.info(f"Generated summary: {summary}")
    save_results(categories, 'results/ner_results.json')
    return entities, categories, summary