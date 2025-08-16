import frappe
# from ....frappe.frappe.model.workflow import apply_workflow
# from frappe import as_json

from frappe.model.workflow import apply_workflow
from frappe import as_json
#from frappe.db import get_value



# def handle_workflow_automation(doc, method):
#     # try:
#     #     apply_workflow(doc, method)
#     # except Exception as e:
#     #     print(f"Auto approval failed: {str(e)}")
#     roles = doc.owner
#     designation = get_value("Employee", {"user_id": doc.owner}, "designation")
#     doc_json = as_json({"doctype": doc.doctype, "name": doc.name})
#     # Only trigger if newly created and in draft
#     if doc.workflow_state == "Draft":
#         if designation == "HR Manager":
#             # HR skips to Approved
#             apply_workflow(doc_json, "Send for Review")      # Draft → Pending Manager
#             apply_workflow(doc_json, "Approve")              # Pending Manager → Pending HR
#             apply_workflow(doc_json, "Approve")              # Pending HR → Approved
#         elif designation == "Manager":
#             # Manager skips to Pending HR
#             apply_workflow(doc_json, "Send for Review")      # Draft → Pending Manager
#             apply_workflow(doc_json, "Approve")              # Pending Manager → Pending HR
#         # else: normal applicant, stays in Pending Manager

def handle_workflow_automation(doc, method):
    #LEAVE
    print(f"[DEBUG] handle_workflow_automation triggered for: {doc.doctype}, Name: {doc.name} {doc.workflow_state}")
    
    roles = doc.owner
    designation = frappe.db.get_value("Employee", {"user_id": doc.owner}, "designation")
    print(f"designation of the user {designation}")
    print(f"[DEBUG] Owner (roles placeholder): {roles}")

    doc_json = as_json({"doctype": doc.doctype, "name": doc.name})
    print(f"[DEBUG] JSON Payload: {doc_json}")

    if doc.workflow_state == "Pending Manager":
        print("[DEBUG] Document is in Draft state")

        if designation == "人事マネージャー":
            print("[DEBUG] Detected HR role, applying workflow steps to reach Approved")

            try:
                # apply_workflow(doc_json, "Send for Review")
                # print("[DEBUG] Applied transition: Send for Review")

                apply_workflow(doc_json, "Approve")
                print("[DEBUG] Applied transition: Approve (1)")

                apply_workflow(doc_json, "Approve")
                print("[DEBUG] Applied transition: Approve (2)")
            except Exception as e:
                print(f"[ERROR] HR workflow automation failed: {e}")

        elif designation == "プロジェクトマネージャー":
            print("[DEBUG] Detected Manager role, applying workflow steps to reach Pending HR")

            try:
                # apply_workflow(doc_json, "Send for Review")
                # print("[DEBUG] Applied transition: Send for Review")

                apply_workflow(doc_json, "Approve")
                print("[DEBUG] Applied transition: Approve")
            except Exception as e:
                print(f"[ERROR] Manager workflow automation failed: {e}")
        else:
            print("[DEBUG] No special role matched; workflow not auto-applied.")
    else:
        print(f"[DEBUG] Document not in Draft state. Current state: {doc.workflow_state}")






def breakfast_allowance(doc,method):
    print(f"[DEBUG] handle_workflow_automation triggered for: {doc.doctype}, Name: {doc.name}")
    
    roles = doc.owner
    designation = frappe.db.get_value("Employee", {"user_id": doc.owner}, "designation")
    print(f"designation of the user {designation}")
    print(f"[DEBUG] Owner (roles placeholder): {roles}")

    doc_json = as_json({"doctype": doc.doctype, "name": doc.name})
    print(f"[DEBUG] JSON Payload: {doc_json}")

    if doc.workflow_state == "Pending Manger":
        if designation == "人事マネージャー":
            print("[DEBUG] Detected HR role, applying workflow steps to reach Approved")
            try:
                # apply_workflow(doc_json, "Send for Review")
                # print("[DEBUG] Applied transition: Send for Review")
                apply_workflow(doc_json, "Approve")
                print("[DEBUG] Applied transition: Approve (2)")
            except Exception as e:
                print(f"[ERROR] HR workflow automation failed: {e}")


def overtime_allowance(doc,method):
    print(f"[DEBUG] handle_workflow_automation triggered for: {doc.doctype}, Name: {doc.name}")
    
    roles = doc.owner
    designation = frappe.db.get_value("Employee", {"user_id": doc.owner}, "designation")
    print(f"designation of the user {designation}")
    print(f"[DEBUG] Owner (roles placeholder): {roles}")

    doc_json = as_json({"doctype": doc.doctype, "name": doc.name})
    print(f"[DEBUG] JSON Payload: {doc_json}")
    # if doc.workflow_state == "Pending Manager":
    #     print("[DEBUG] Document is in Draft state")
        
    if designation == "人事マネージャー":
        print("[DEBUG] Detected HR role, applying workflow steps to reach Approved")

        try:
            # apply_workflow(doc_json, "Send for Review")
            # print("[DEBUG] Applied transition: Send for Review")
            if doc.workflow_state == "~ Pending Manager":
                apply_workflow(doc_json, "Approve and Request More Info")
                print("[DEBUG] Applied transition : Approve and Request More Info")
            if doc.workflow_state == "Pending Hr":
                # apply_workflow(doc_json, "Send for Final Review")
                # print("[DEBUG] Applied transition: Send for Final Review")
                apply_workflow(doc_json, "Approve")
                print("[DEBUG] Applied transition: Approve (1)")

                # apply_workflow(doc_json, "Approve")
                # print("[DEBUG] Applied transition: Approve (2)")
        except Exception as e:
            print(f"[ERROR] HR workflow automation failed: {e}")