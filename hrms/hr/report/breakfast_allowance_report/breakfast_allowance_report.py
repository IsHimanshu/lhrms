# Copyright (c) 2023, MacBease and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    # Define the report columns
    columns = [
        {"label": "Employee ID", "fieldname": "employee_id", "fieldtype": "Data", "width": 120},
        {"label": "Username", "fieldname": "username", "fieldtype": "Data", "width": 150},
        {"label": "Month", "fieldname": "select_month", "fieldtype": "Data", "width": 100},
        {"label": "Max Allowance", "fieldname": "max_allowance_range", "fieldtype": "Data", "width": 120},
        {"label": "Total Days", "fieldname": "total_days", "fieldtype": "Int", "width": 100},
        {"label": "Status", "fieldname": "workflow_state", "fieldtype": "Data", "width": 100},
    ]

    # Optional: Handle filters (e.g., by username or month)
    conditions = ""
    if filters.get("username"):
        conditions += f" AND username = {frappe.db.escape(filters.get('username'))}"

    # Fetch the data
    data = frappe.db.sql(f"""
        SELECT
            employee_id,
            username,
            select_month,
            max_allowance_range,
            total_days,
            workflow_state
        FROM `tabBreakfast`
        WHERE docstatus < 2
        {conditions}
        ORDER BY creation DESC
    """, as_dict=True)

    return columns, data
