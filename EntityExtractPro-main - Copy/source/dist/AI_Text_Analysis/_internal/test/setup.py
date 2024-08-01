import sys
import subprocess
import os

def install_requirements():
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def download_spacy_model():
    print("Downloading SpaCy model...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

def create_directories():
    print("Creating necessary directories...")
    for directory in ['logs', 'results', 'highlighted']:
        os.makedirs(directory, exist_ok=True)

def main():
    print("Setting up EntityExtract Pro...")
    install_requirements()
    download_spacy_model()
    create_directories()
    print("Setup complete!")

if __name__ == "__main__":
    main()