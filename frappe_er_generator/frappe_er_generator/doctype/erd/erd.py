# Copyright (c) 2024, Sumit Jain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe_er_generator.frappe_er_generator.er_generator import get_erd


class ERD(Document):
    def validate(self):
        self.validate_directory()
        if self.doctypes:
            doctypes = (
                list(map(str.strip, self.doctypes.split(",")))
                if "," in self.doctypes
                else [self.doctypes.strip()]
            )
        else:
            doctypes = None
        if self.doctype_substrings:
            str_in = (
                list(map(str.strip, self.doctype_substrings.split(",")))
                if "," in self.doctype_substrings
                else [self.doctype_substrings.strip()]
            )
        else:
            str_in = None

        file, matches = get_erd(doctypes=doctypes, str_in=str_in, site=True)
        self.doctype_matches = str(("\n").join(matches))
        self.image = file.file_url

    def validate_directory(self):
        if not frappe.db.exists("File", {"is_folder": 1, "name": "Home/ERD"}):
            frappe.new_doc("File", file_name="ERD", is_folder=1).insert()
