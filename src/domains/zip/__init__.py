import os
import zipfile
from pathlib import Path
from flask import send_file

class ZipManager(object):
   def __init__(self, output_base="outputs"):
       self.output_base = Path(__file__).parent.parent.parent.parent / output_base
       os.makedirs(self.output_base, exist_ok=True)

   def create_zip_from_folder(self, folder_name):
       """
       Creates a zip from folder_name inside output_base.
       Returns Flask send_file response with cleanup.
       """
       folder_path = os.path.join(self.output_base, folder_name)
       if not os.path.exists(folder_path):
           raise FileNotFoundError(f"Folder {folder_path} does not exist.")

       zip_path = os.path.join(folder_path, f"{folder_name}.zip")
       
       # Create the zip with correct folder structure
       with zipfile.ZipFile(zip_path, "w") as zipf:
           for root, dirs, files in os.walk(folder_path):
               for file_name in files:
                   if file_name != 'checklist.txt':
                       continue
                   file_path = os.path.join(root, file_name)
                   arcname = os.path.relpath(file_path, self.output_base)
                   zipf.write(file_path, arcname)
       # Send file with cleanup after download
       response = send_file(zip_path, as_attachment=True, download_name=f"{folder_name}.zip")

       @response.call_on_close
       def cleanup():
           try:
               os.remove(zip_path)
               for f in os.listdir(folder_path):
                   os.remove(os.path.join(folder_path, f))
               os.rmdir(folder_path)
           except Exception as e:
               print(f"[ZipManager] Cleanup failed: {e}")

       return response