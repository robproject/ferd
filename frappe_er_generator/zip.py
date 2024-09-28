import frappe
import os
import shutil
import zipfile
from frappe.utils import get_site_base_path


@frappe.whitelist()
def get_zip(name, string):
    p = os.getcwd()
    try:
        os.chdir("..")
        temp_dir = os.path.join("/tmp", f"temp_{name}")
        os.makedirs(temp_dir, exist_ok=True)

        temp_path = os.path.join(temp_dir, name)
        shutil.copytree(f"{os.getcwd()}{string}", temp_path)

        # Create a zip file
        zip_filename = f"{name}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(temp_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_path)
                    zipf.write(file_path, arcname)

        # Read the zip file content
        with open(zip_path, "rb") as file:
            file_content = file.read()

        # Create a File document
        os.chdir("sites")
        file_doc = frappe.new_doc(
            "File",
            file_name=zip_filename,
            content=file_content,
            is_private=1,
        ).insert()
        print(file_doc)

        # Clean up temporary directory

    except Exception as e:
        return {"success": False, "message": str(e)}
    finally:
        shutil.rmtree(temp_dir)
        os.chdir(p)
        frappe.db.commit()
