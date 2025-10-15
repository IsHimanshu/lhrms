# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe

class arssupportissue(Document):
	#
	def validate(self):
		# frappe.msgprint(
		# 		("Warning - triggered}: "),
		# 		indicator="orange",
		# 		alert=True,
		# 	)
		for i in self.table_vzjv:
			if self.client_id and not i.client_id:
				i.client_id = self.client_id

	def update_time_and_costing(self):
		frappe.msgprint(
				("Warning - here is the fetched issue_name {0}: ").format(self.name),
				indicator="orange",
				alert=True,
			)
		# Fetch timesheet details linked to this issue
		tl = frappe.db.sql(
			"""
			select 
				min(from_time) as start_date, 
				max(to_time) as end_date,
				sum(billing_amount) as total_billing_amount, 
				sum(costing_amount) as total_costing_amount,
				sum(hours) as time
			from `tabSupport Timesheet Details`
			where issue = %s and docstatus = 1  
			""",  #removed docstatus = 1
			self.name,
			as_dict=1,
		)[0]
		frappe.msgprint(
				("Warning - here is the fetched recors {0}: ").format(tl),
				indicator="orange",
				alert=True,
			)
		self.flags.ignore_validate_update_after_submit = True
		frappe.db.set_value(
			self.doctype,
			self.name,
			{
				"total_costing_amount": tl.total_costing_amount or 0,
				"total_billing_amount": tl.total_billing_amount or 0,
				"actual_time": tl.time or 0,
				"act_start_date": tl.start_date,
				"act_end_date": tl.end_date,
			},
			update_modified=False,
		)
		self.reload()

	# def has_permission(self, permtype="read", *, debug=True, user=None) -> bool:
	# 	if "ARS support" in frappe.get_roles(user):
	# 		print(f"Warning - here is the fixed {user}")
	# 		return True
	# 	return False


# def has_user_permission(self, user=None, ptype=None):
# 	frappe.logger().info(f"Checking has_permission for {self.name}, user={user}")
# 	if not user:
# 		user = frappe.session.user
# 	if "ARS support" in frappe.get_roles(user):
# 		return True
# 	from frappe.permissions import has_user_permission as frappe_has_user_permission
# 	return frappe_has_user_permission(self, user=user, ptype=ptype)



# def get_permission_query_conditions(user):
# 	if "ARS support" in frappe.get_roles(user):
# 		print(f"Warning - here is the fixed  no restrictionssssss for    {user}")
# 		return None  
# 	return "1=0" 

import json

@frappe.whitelist()
def issue_search(doctype=None, txt="", searchfield=None, start=0, page_len=20, filters=None):
	conditions = []
	values = {
	"txt": f"%{txt}%",
	"start": start,
	"page_len": page_len,
	}
	if isinstance(filters, str):
		try:
			filters = json.loads(filters)
		except Exception:
			filters = {}
	filters = filters or {}
	match_case = """
	CASE
		WHEN iss.name LIKE %(txt)s THEN 'ID'
		WHEN iss.subject LIKE %(txt)s THEN '件名'
		WHEN iss.product_name LIKE %(txt)s THEN '製品名'
		WHEN iss.inquiry_handler_name LIKE %(txt)s THEN '担当者'
		WHEN iss.development_representative_name LIKE %(txt)s THEN '開発担当者名前'
		WHEN iss.issue_opening_date LIKE %(txt)s THEN 'Opening Date'
		WHEN iss.issue_closing_date LIKE %(txt)s THEN 'Closing Date'
		WHEN iss.client_name LIKE %(txt)s THEN '取引先名'
		WHEN child.case_data LIKE %(txt)s THEN '問合せ内容'
		WHEN child.case_reply LIKE %(txt)s THEN '回答'
		ELSE 'Other'
			END
		"""
	conditions.append("""
			(iss.name LIKE %(txt)s
			OR iss.subject LIKE %(txt)s
			OR iss.product_name LIKE %(txt)s
			OR iss.inquiry_handler_name LIKE %(txt)s
			OR iss.development_representative_name LIKE %(txt)s
			OR iss.issue_opening_date LIKE %(txt)s
			OR iss.issue_closing_date LIKE %(txt)s
			OR iss.client_name LIKE %(txt)s
			OR EXISTS (
             SELECT 1 FROM `tabars_support_issue_table` child
             WHERE child.parent = iss.name
               AND (child.case_data LIKE %(txt)s
                    OR child.case_reply LIKE %(txt)s
					)
         	))
			""")
	if filters:
		for key, val in filters.items():
			conditions.append(f"`{key}` = %({key})s")
			values[key] = val
	where_clause = " AND ".join(conditions)
	return frappe.db.sql(
						f"""
						SELECT iss.name, iss.subject , iss.inquiry_handler_name,
						CONCAT({match_case},
						IFNULL(CONCAT(' → "', 
							CASE 
                           WHEN child.case_data LIKE %(txt)s THEN child.case_data
                           WHEN child.case_reply LIKE %(txt)s THEN child.case_reply
						END, '"'), '')
								) as info
						FROM `tabars support issue` iss
						LEFT JOIN `tabars_support_issue_table` child
							ON child.parent = iss.name
							AND (child.case_data LIKE %(txt)s OR child.case_reply LIKE %(txt)s)
						WHERE {where_clause}
						ORDER BY iss.modified DESC
						LIMIT %(start)s, %(page_len)s
						""",
						values,
						)
