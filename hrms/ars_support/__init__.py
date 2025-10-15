# import frappe
# import frappe.core.doctype.user_permission.user_permission as up
# from hrms.ars_support import per

# # Force monkey patch
# up.get_user_permissions = per.get_user_permissions

# # Also make sure whitelisted registry points to yours
# frappe.whitelist()(per.get_user_permissions)
