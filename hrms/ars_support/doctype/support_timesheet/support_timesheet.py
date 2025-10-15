# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe

from frappe.utils import flt, get_datetime, getdate

class OverlapError(frappe.ValidationError):
	pass


class OverWorkLoggedError(frappe.ValidationError):
	pass


class SupportTimesheet(Document):
	#pass
	def validate(self):
		self.validate_dates()
		self.calculate_hours()
		self.validate_time_logs()
		self.update_cost()
		self.calculate_total_amounts()
		self.set_dates()
		
		#self.update_issue_and_project()

	def calculate_hours(self):
		for row in self.time_logs:
			if row.to_time and row.from_time:
				row.calculate_hours()
				row.validate_billing_hours()
				row.update_billing_hours()


	def set_dates(self):
		if self.docstatus < 2 and self.time_logs:
			start_date = min(getdate(d.from_time) for d in self.time_logs)
			end_date = max(getdate(d.to_time) for d in self.time_logs)

			if start_date and end_date:
				self.start_date = getdate(start_date)
				self.end_date = getdate(end_date)

	def validate_dates(self):
		for time_log in self.time_logs:
			time_log.validate_dates()

	def validate_time_logs(self):
		for time_log in self.time_logs:
			time_log.set_to_time()
			time_log.validate_issue_man()
			#self.validate_overlap(time_log)
			#time_log.set_project()
			#time_log.validate_parent_project(self.parent_project)
			#time_log.validate_task_project()
			if time_log.issue and time_log.project:
				linked_project = frappe.db.get_value("ars support issue", time_log.issue, "project")
				if not linked_project:
					frappe.throw(
						f"In row {time_log.idx}: Issue '{time_log.issue}' is not linked to any Project.",
						title="Missing Project for Issue"
					)
				if linked_project and linked_project != time_log.project:
					frappe.throw(
						f"In row {time_log.idx}: Project '{time_log.project}' does not match the one linked to Issue '{time_log.issue}' (expected '{linked_project}').",
						title="Invalid Project for Issue"
					)

	def calculate_total_amounts(self):
		self.total_hours = 0.0
		self.total_billable_hours = 0.0
		self.total_billed_hours = 0.0
		self.total_billable_amount = self.base_total_billable_amount = 0.0
		self.total_costing_amount = self.base_total_costing_amount = 0.0
		self.total_billed_amount = self.base_total_billed_amount = 0.0

		for d in self.get("time_logs"):
			d.update_billing_hours()
			self.update_time_rates(d)

			self.total_hours += flt(d.hours)
			self.total_costing_amount += flt(d.costing_amount)
			self.base_total_costing_amount += flt(d.base_costing_amount)
			if d.is_billable:
				self.total_billable_hours += flt(d.billing_hours)
				self.total_billable_amount += flt(d.billing_amount)
				self.base_total_billable_amount += flt(d.base_billing_amount)
				self.total_billed_amount += flt(d.billing_amount) if d.sales_invoice else 0.0
				self.base_total_billed_amount += flt(d.base_billing_amount) if d.sales_invoice else 0.0
				self.total_billed_hours += flt(d.billing_hours) if d.sales_invoice else 0.0

	def update_time_rates(self, ts_detail):
		if not ts_detail.is_billable:
			ts_detail.billing_rate = 0.0
	def update_cost(self):
		for time_log in self.time_logs:
			time_log.update_cost(self.employee)			
	def on_submit(self):
		#print("On Submit hook trigeeered")
		#self.validate_mandatory_fields()
		self.update_issue_and_project()
		for tl in self.time_logs:
			tl.valVirtual()
	def on_cancel(self):
		#print("On Submit hook trigeeered")
		#self.validate_mandatory_fields()
		self.update_issue_and_project()
	
	def update_issue_and_project(self):
		issues, projects = [], []

		for data in self.time_logs:
			
			if data.issue and data.issue not in issues:
				issue = frappe.get_doc("ars support issue", data.issue)
				frappe.msgprint(
				("Warning - here is the fetched recors {0}: ").format(data.name),
				indicator="orange",
				alert=True,
				)
				#implement this function in issue doctype
				#if hasattr(issue, "update_time_and_costing"):
				issue.update_time_and_costing()

			
				# time_logs_completed = all(
				# 	tl.completed for tl in self.time_logs if tl.issue == issue.name
				# )

				# issue.status = "Closed" if time_logs_completed else "Open"
				issue.save(ignore_permissions=True)

				issues.append(data.issue)

			
			if data.project and data.project not in projects:
				projects.append(data.project)
		for project in projects: 
			project_doc = frappe.get_doc("Project", project)
			#project_doc.update_project() #add a support cost field and refactor the cost callculation to add support cost there
			project_cost  = frappe.db.sql(
                    """
                    SELECT sum(billing_amount) as issue_expense
                    FROM `tabSupport Timesheet Details`
                    WHERE project = %s AND docstatus = 1
                    """,
                    project,
                    as_dict=1,
                )[0]
			project_doc.db_set("issue_expense", project_cost.issue_expense or 0)
			project_doc.save(ignore_permissions=True)
