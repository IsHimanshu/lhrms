# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

import frappe

from datetime import datetime

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
	#pass
	def validate(self):
		self.validate_same_month_leave()

	def validate_same_month_leave(self):
		if self.start_date and self.end_date:
			from_date = str(self.start_date)[:7]
			to_date =str(self.end_date)[:7]
			if (from_date != to_date):
				frappe.throw(
				"休暇申請は月をまたぐことはできません。翌月分は別の申請を作成してください。"
				)