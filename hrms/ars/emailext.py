import frappe

@frappe.whitelist(allow_guest=True)
def allowedemailuser():
    
    doctype = frappe.form_dict.get("doctype") or "Leave"
    docname = frappe.form_dict.get("docname") or "cp2mlm4f0b"
    role = frappe.form_dict.get("role")
    print(f"Doctypes i got {doctype} {docname} {role}")
    
    user_list = frappe.get_all("User", filters={"enabled": 1}, pluck="name")
    if role:
        role_users = frappe.get_all("Has Role", filters={"role": role}, pluck="parent")
        user_list = list(set(user_list) & set(role_users))
    
    allowed_users = []
    doc = frappe.get_doc(doctype, docname)
    for user in user_list:
        if frappe.has_permission(doctype=doctype, ptype="read", user=user, doc=doc):
            allowed_users.append(user)
    
    return allowed_users


def allowedemailuserf(docname,doctype,role):
    
    # doctype = frappe.form_dict.get("doctype") #or "Leave"
    # docname = frappe.form_dict.get("docname") #or "cp2mlm4f0b"
    # role = frappe.form_dict.get("role")
    print(f"Doctypes i got {doctype} {docname} {role}")
    
    user_list = frappe.get_all("User", filters={"enabled": 1}, pluck="name")
    if role:
        role_users = frappe.get_all("Has Role", filters={"role": role}, pluck="parent")
        user_list = list(set(user_list) & set(role_users))
    
    allowed_users = []
    doc = frappe.get_doc(doctype, docname)
    for user in user_list:
        if frappe.has_permission(doctype=doctype, ptype="read", user=user, doc=doc):
            allowed_users.append(user)
    
    return allowed_users