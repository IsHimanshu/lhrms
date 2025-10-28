# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe import _

class Overtime(Document):
	def validate(self):
		self.validate_hours()
	
	def validate_hours(self):
		for row in self.overtime_table:
			row.validate_time()


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
