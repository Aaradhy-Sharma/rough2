import spacy
from pathlib import Path
import shutil

def download_spacy_model(model_name, target_dir):
    # Download the model if not already present
    spacy.cli.download(model_name)
    # Get the path to the model
    model_path = spacy.util.get_package_path(model_name)
    # Copy the model to the target directory
    target_model_path = Path(target_dir) / model_name
    if target_model_path.exists():
        shutil.rmtree(target_model_path)
    shutil.copytree(model_path, target_model_path)

download_spacy_model("en_core_web_sm", ".")
