import frappe

def send_virtual_issue_related_reminders():
    #frappe.log_error("Scheduler triggered!", "Scheduler Test")
    timesheets = frappe.db.sql("""
        SELECT DISTINCT parent
        FROM `tabSupport Timesheet Details`
        WHERE work_type = '課題対応(CSMS未登録)'
    """, as_dict=True)
    frappe.log_error(f"Timesheets found: {timesheets}", "Virtual Issue Debug")
    for ts in timesheets:
        try:
            ts_doc = frappe.get_doc("Support Timesheet", ts.parent)

            if not ts_doc.owner:
                #frappe.log_error("email not found")
                continue  
            frappe.log_error(f"Processing {ts_doc.name}, email={ts_doc.owner}", "Virtual Issue Debug")

            
            site_url = frappe.utils.get_url()
            ts_link = f"{site_url}/app/support-timesheet/{ts_doc.name}"

            
            # message = f"""
            #     <p>ご担当者様,</p>
            #     <p>以下のタイムシートに「Issue Related」の作業ログが登録されています。</p>
            #     <p>
            #         タイムシート番号: <b>{ts_doc.name}</b><br>
            #         リンク: <a href="{ts_link}">{ts_link}</a>
            #     </p>
            #     <p>ご確認をお願いいたします。</p>
            # """
            
            message = f"""
                    <p>ご担当者様,</p>
                    <p>以下のタイムシートに「Issue Related」の作業ログが登録されています。</p>
                    <p>
                        タイムシート番号: <b>{ts_doc.name}</b><br>
                        リンク: <a href="{ts_link}">{ts_link}</a>
                    </p>
                    <p>
                        つきましては、該当するバーチャルIssueを実際のIssueに変換いただきますようお願いいたします。
                    </p>
                    <p>ご対応のほど、よろしくお願い申し上げます。</p>
                """


            frappe.sendmail(
                recipients=[ts_doc.owner],
                subject=f"タイムシート {ts_doc.name} - Issue Related 作業ログのお知らせ",
                message=message,
                now = True
            )
            frappe.log_error(f"Mail sent to {ts_doc.owner}", "Virtual Issue Debug")

        except Exception as e:
            frappe.log_error(f"Error sending email for timesheet {ts_doc.name}: {e}", "Virtual Issue Reminder Email Error")
