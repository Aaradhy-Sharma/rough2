from cx_Freeze import setup, Executable
import os
import shutil
import spacy

# Copy the spaCy model to the project directory
model_name = "en_core_web_sm"
model_path = spacy.util.get_package_path(model_name)
shutil.copytree(model_path, os.path.join(os.getcwd(), model_name))

# Include the spaCy model and other files in the data_files
data_files = [
    (model_name, [os.path.join(model_name, file) for file in os.listdir(model_name)]),
    ('.', ['.DS_Store', 'AI_Text_Analysis.spec', 'app.py', 'azure.tcl', 'build.sh', 'EntityExtract Pro build script.txt', 'EntityExtract Pro packaging.py', 'gui.py', 'gui1.py', 'light.tcl', 'main.py', 'NERApp.spec', 'requirements.txt', 'text_analysis.py', 'utils.py']),
]

# Function to include entire directories
def add_dir_to_data_files(source_dir, target_dir):
    for root, _, files in os.walk(source_dir):
        target_path = os.path.join(target_dir, os.path.relpath(root, source_dir))
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        for file in files:
            data_files.append((target_path, [os.path.join(root, file)]))

# Add directories to data_files
add_dir_to_data_files('AI_Text_Analysis_Package', 'AI_Text_Analysis_Package')
add_dir_to_data_files('azure', 'azure')
add_dir_to_data_files('highlighted', 'highlighted')
add_dir_to_data_files('logs', 'logs')
add_dir_to_data_files('results', 'results')
add_dir_to_data_files('test', 'test')

# Setup configuration for cx_Freeze
setup(
    name="AI_Text_Analysis",
    version="1.0",
    description="AI Text Analysis Application",
    options={
        "build_exe": {
            "packages": ["tkinter", "spacy"],
            "include_files": data_files,
        }
    },
    executables=[Executable("main.py", base="Win32GUI")],  # Use "Win32GUI" for GUI apps
)
