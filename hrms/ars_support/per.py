import frappe
from frappe.core.doctype.user_permission.user_permission import (
		get_user_permissions as _get_user_permissions,
	)


import frappe
from frappe.core.doctype.user_permission.user_permission import (
    get_user_permissions as _get_user_permissions,
)

@frappe.whitelist()
def get_user_permissions(user=None):
    user = user or frappe.session.user
    out = _get_user_permissions(user)
    print(f"[DEBUG] ARS support override for {user} before removing is {out}")
    if "ARS support" in frappe.get_roles(user):
        print(f"[DEBUG] ARS support override for {user}")
        if "Employee" in out:
            del out["Employee"]
            print(f"[DEBUG] ARS support override for {user} after removing is {out}")
    return out