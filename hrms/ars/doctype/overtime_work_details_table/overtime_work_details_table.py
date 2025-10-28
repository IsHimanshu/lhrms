# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class Overtimeworkdetailstable(Document):
	def validate_time(self):
		#frappe.msgprint(f"Validating time: {self.end_time} - {self.start_time}")
		if str(self.end_time) <= str(self.start_time):
			frappe.throw(frappe._("End date/time must be later than Start date/time."))
