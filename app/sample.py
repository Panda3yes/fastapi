import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
import os

def open_revit_project(file_name):
    try:
        # Get the directory of the script
        script_directory = os.path.dirname(__file__)
        
        # Construct the full path to the Revit project file
        file_path = os.path.join(script_directory, file_name)
        
        # Open the Revit project file
        app = DocumentManager.Instance.CurrentUIApplication.Application
        options = OpenOptions()
        options.Audit = False
        options.DetachFromCentralOption = DetachFromCentralOption.DoNotDetach
        doc = app.OpenDocumentFile(file_path, options)
        return doc
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    # Provide the relative path to the Revit project file
    file_name = "YourRevitProject.rvt"  # Change this to the name of your Revit project file
    
    # Call the function to open the Revit project
    opened_document = open_revit_project(file_name)
    if isinstance(opened_document, Document):
        print("Revit project opened successfully.")
    else:
        print("Error:", opened_document)