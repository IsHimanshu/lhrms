# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
import datetime

class Overtimeworkdetailstable(Document):
	def validate_time(self):
		#frappe.msgprint(f"Validating time: {self.end_time} - {self.start_time}")
		if str(self.end_time) <= str(self.start_time):
			frappe.throw(frappe._("End date/time must be later than Start date/time."))
	def validate_holiday(self,start_limit,end_limit):
		#frappe.msgprint(f"Validating time: {self.end_time} - {self.start_time}")
		start_dt = (
		datetime.datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S")
		if isinstance(self.start_time, str)
		else self.start_time
		)
		end_dt = (
		datetime.datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S")
		if isinstance(self.end_time, str)
		else self.end_time
		)
		if not (start_limit < end_dt <= end_limit):
			frappe.throw(frappe._(f" これが午前5時に達したら、別の申請を出してください。"))

