# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_to_date, flt, get_datetime, time_diff_in_hours, time_diff_in_seconds

class SupportTimesheetDetails(Document):
	def set_to_time(self):
		"""Set to_time based on from_time and hours."""
		if not (self.from_time and self.hours):
			return

		_to_time = get_datetime(add_to_date(self.from_time, hours=self.hours, as_datetime=True))
		if abs(time_diff_in_seconds(_to_time, self.to_time)) >= 1:
			self.to_time = _to_time
	
	def calculate_hours(self):
		"""Calculate hours based on from_time and to_time."""
		if self.to_time and self.from_time:
			self.hours = time_diff_in_hours(self.to_time, self.from_time)
	
	def validate_dates(self):
		"""Validate that to_time is not before from_time..."""
		if self.from_time and self.to_time and time_diff_in_hours(self.to_time, self.from_time) < 0:
			frappe.throw(frappe._("To Time cannot be before from date"))

	def update_billing_hours(self):
		"""Update billing hours based on hours."""
		if not self.is_billable:
			self.billing_hours = 0
			return

		if flt(self.billing_hours) == 0.0:
			self.billing_hours = self.hours
	

	def update_cost(self, employee: str):
		"""Update costing and billing rates based on activity type."""
		#from erpnext.projects.doctype.timesheet.timesheet import get_activity_cost

		if not self.is_billable and not self.activity_type:
			return
		a = frappe.get_doc("Employee",employee)
		rate = a.billing_rate
		print("here is the fetched rateee",rate) 	
		# frappe.msgprint(
		# 		("Warning - here is the fetched ratee {0}: ").format(rate),
		# 		indicator="orange",
		# 		alert=True,
		# 	)
			#get_activity_cost(employee, self.activity_type)
		if not rate:
			return

		self.billing_rate =  rate#(
		# 	flt(rate) if flt(self.billing_rate) == 0 else self.billing_rate
		# )
		# self.costing_rate = (
		# 	flt(rate.get("costing_rate")) if flt(self.costing_rate) == 0 else self.costing_rate
		# )
		print(self.billing_rate * (self.billing_hours or 0))
		self.billing_amount = self.billing_rate * (self.billing_hours or 0)
		#self.costing_amount = self.costing_rate * (self.billing_hours or self.hours or 0)

	def validate_billing_hours(self):
		"""Warn if billing hours are more than actual hours."""
		if flt(self.billing_hours) > flt(self.hours): 
			frappe.msgprint(
				frappe._("Warning - Row {0}: Billing Hours are more than Actual Hours").format(self.idx),
				indicator="orange",
				alert=True,
			)

	def validate_issue_man(self):
		if self.work_type == "課題対応(CSMS登録済)" and self.issue is None or self.issue =="":  #"Issue Related":
			frappe.throw(frappe._("Issue is Mandatory when issue related work"))
	
	def valVirtual(self):
		if self.work_type == "課題対応(CSMS未登録)":     #"Virtual Issue Related":
			frappe.throw(frappe._("You can't submit timesheet when virtual issue is there."))