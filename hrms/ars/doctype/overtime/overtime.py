# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe import _
import datetime

from datetime import timedelta

class Overtime(Document):
	def validate(self):
		self.validate_hours()
		self.validate_holiday()
	
	def validate_hours(self):
		for row in self.overtime_table:
			row.validate_time()


	def validate_holiday(self):
		if self.shift == "所定休日":
			if isinstance(self.start_date, str):
				start_time = datetime.datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
			else:
				start_time = self.start_date
			if isinstance(self.end_date, str):
				end_dt = datetime.datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S")
			else:
				end_dt = self.end_date
			start_limit = start_time.replace(hour=5, minute=0, second=0, microsecond=0)
			end_limit = start_limit + timedelta(days=1)  # next day 5:00 AM

			# Check if start_time is within allowed window
			if not (start_limit < end_dt <= end_limit):
				frappe.throw(_("これが午前5時に達したら、別の申請を出してください。."))
			if self.overtime_table:
				#start_date = self.overtime_table[0].start_time
				# if isinstance(start_date,str):
				# 	start_time = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
				# else:
				# 	start_time = start_date
				#start_limit = start_time.replace(hour=5, minute=0, second=0, microsecond=0)
				#end_limit = start_limit + timedelta(days=1)  # next day 5:00 AM
				for row in self.overtime_table:
					row.validate_holiday(start_limit,end_limit)



@frappe.whitelist()
def convert_to_leave(docname):
	overtime = frappe.get_doc("Overtime", docname)

	if not overtime.employee_id:
		frappe.throw(_("Employee is required to create leave"))

	if overtime.today_total_working_hour < 480:
		frappe.throw(_(f"Leave can only be created when actual hours is greater than 8 and your hours are {overtime.today_total_working_hour/60}"))

	
	leave = frappe.new_doc("Leave")
	leave.employee_id = overtime.employee_id
	leave.date = frappe.utils.today()
	leave.leave_type = "代休"
	# overtime.remove_mins += 480
	# overtime.save()
	overtime.overtime_adjustment = "休暇"
	overtime.save()
	leave.save()
	return leave.name
