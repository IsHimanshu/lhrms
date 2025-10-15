# import frappe
# from frappe import _
# from hrms.ars.emailext import allowedemailuserf

# def get_role_from_workflow_state(doc):
#     role = ""
#     if doc.workflow_state == "Pending HR":
#         role = "Ars HR"
#         print(role)
#     elif doc.workflow_state == "Pending Manager":
#         role = "Ars Manager"
#         print(role)
#     else:
#         print("Cannot send mail : ", doc.workflow_state)
#     return role


# def get_filtered_email_list(doc, role):
#     print("Mail melega re ruk toh :",doc.name,doc.doctype,role)
#     try:
#         # Get email list from frappe call
#         # response = frappe.call({
#         #     args:{
#         #     "hrms.ars.emailext.allowedemailuser",
#         #     docname=doc.name,
#         #     doctype=doc.doctype,
#         #     role=role
#         # }})
        
#         response = allowedemailuserf(docname=doc.name,
#                                     doctype=doc.doctype,
#                                     role = role)

#         if not response:
#             print("Error: No response or method failed")
#             return []
        
#         print("role : ", response)
        
#         # Filter out admins
#         owner = doc.owner
#         ceo = "tsune@ar-system.co.jp"
#         hr_manager = "m-tanaka@ar-system.co.jp"
#         administrator = "Administrator"
#         admins = [owner, hr_manager, ceo, administrator]
        
#         filtered_list = [email for email in response if not any(
#             admin in email for admin in admins)]
        
#         return filtered_list
        
#     except Exception as e:
#         print("Error:", str(e))
#         return []


# def send_notification(doc=None, demail=None):
#     print("document : ", doc)
#     if doc and doc.workflow_state not in ["Pending HR", "Pending Manager"]:
#         print("Skipiing mail workflow_state not matched...")
#         return
    
#     print("this is final approver mail : ", demail)
#     recipient = "ankitjarwalll@gmail.com"

#     subject_template = "休暇等申請書 {{ workflow_state }}"
#     context = {
#         "role":demail,
#         "name1": doc.name1,
#         "date": doc.date,
#         "leave_type": doc.leave_type,
#         "start_date": doc.start_date,
#         "end_date": doc.end_date,
#         "days_difference": doc.days_difference,
#         "workflow_state": doc.workflow_state,
#         "form_url": frappe.utils.get_url_to_form(doc.doctype, doc.name)
#     }
#     subject = frappe.render_template(subject_template, context)
#     print("subject : ", context)

#     message_template = """
#     <div style="font-family: Arial, sans-serif; color: #333; max-width: 640px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
#       <h2 style="color: #4a90e2; border-bottom: 1px solid #eee; padding-bottom: 8px;">📝 休暇等申請書</h2>

#       <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
#         <tr>
#           <td style="padding: 8px; border: 1px solid #eee;"><strong>role</strong></td>
#           <td style="padding: 8px; border: 1px solid #eee;">{{ role }}</td>
#         </tr>
#         <tr>
#           <td style="padding: 8px; border: 1px solid #eee;"><strong>作成者</strong></td>
#           <td style="padding: 8px; border: 1px solid #eee;">{{ name1 }}</td>
#         </tr>
#         <tr>
#           <td style="padding: 8px; border: 1px solid #eee;"><strong>申請日</strong></td>
#           <td style="padding: 8px; border: 1px solid #eee;">{{ date }}</td>
#         </tr>
#         <tr>
#           <td style="padding: 8px; border: 1px solid #eee;"><strong>区分</strong></td>
#           <td style="padding: 8px; border: 1px solid #eee;">{{ leave_type }}</td>
#         </tr>
#         <tr>
#           <td style="padding: 8px; border: 1px solid #eee;"><strong>休暇日（から）</strong></td>
#           <td style="padding: 8px; border: 1px solid #eee;">{{ start_date }}</td>
#         </tr>
#         <tr>
#           <td style="padding: 8px; border: 1px solid #eee;"><strong>休暇期間</strong></td>
#           <td style="padding: 8px; border: 1px solid #eee;">{{ days_difference }}</td>
#         </tr>
#         <tr>
#           <td style="padding: 8px; border: 1px solid #eee;"><strong>状態</strong></td>
#           <td style="padding: 8px; border: 1px solid #eee;">{{ workflow_state }}</td>
#         </tr>
#       </table>
#       <p style="margin-top: 20px;">この休暇申請をレビューまたは承認するには、以下のリンクをクリックしてください</p>
#       <p style="margin-top: 10px;">
#         <a href="{{ form_url }}" style="display: inline-block; padding: 10px 20px; background-color: #4a90e2; color: #fff; text-decoration: none; border-radius: 5px;">休暇申請を見る</a>
#       </p>
#       <p style="margin-top: 10px;">ご不明な点がございましたら、直属の上司までご連絡ください。</p>

#       <hr style="margin-top: 30px;">
#       <p style="font-size: 12px; color: #888;">こちらは自動送信メールです。直接のご返信はご遠慮ください。</p>
#     </div>
#     """

#     message = frappe.render_template(message_template, context)

#     frappe.sendmail(
#         recipients=recipient,
#         subject=subject,
#         message=message,
#         header=[_("Leave Application"), "info"]
#     )


# def start_email_sending(doc,method):
#     print(f"DEBUG email triggered for doc.name, doc.doctype , doc.name1")
#     role = get_role_from_workflow_state(doc)
#     final_email = get_filtered_email_list(doc, role)
#     print("Final email :", final_email)
#     send_notification(doc, final_email)

# #start_email_sending()

def exclude_permission_for_support(user, doc):
    # If user is a specific role, allow access to this DocType regardless
    if "ARS support" in frappe.get_roles(user):
        return True
    return False