# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

import frappe

# def has_permission(doc, ptype, user):
#     if frappe.has_role("CEO", user) or frappe.has_role("HR Manager", user):
#         return True
#     if doc.owner == user:
#         return True
#     department = frappe.get_doc("Department", doc.department)
#     if department.department_head == user:
#         return True
#     return False
class Leave(Document):
	pass