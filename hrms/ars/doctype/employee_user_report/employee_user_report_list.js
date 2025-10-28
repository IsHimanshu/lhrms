frappe.listview_settings["Employee User Report"] = {
  onload(listview) {
    listview.page.add_inner_button(__("Generate All Employee PDFs"), () => {
      const d = new frappe.ui.Dialog({
        title: __("Generate All Employee PDFs"),
        fields: [
          {
            fieldname: "select_from",
            label: __("From Datetime"),
            fieldtype: "Datetime",
            reqd: 1,
          },
          {
            fieldname: "select_to",
            label: __("To Datetime"),
            fieldtype: "Datetime",
            reqd: 1,
          },
        ],
        primary_action_label: __("Generate"),
        primary_action(values) {
          if (!values.select_from || !values.select_to) {
            frappe.msgprint({ message: __("Please fill both datetimes."), indicator: "red" });
            return;
          }

          d.set_primary_action(__("Generating..."));
          d.get_primary_btn().prop("disabled", true);

          frappe.call({
            // TODO: update to your actual dotted path
            method: "hrms.ars.doctype.employee_user_report.api.generate_all_employee_reports",
            args: {
              from_date: values.select_from, // Datetime string
              to_date: values.select_to,     // Datetime string
            },
            freeze: true,
            freeze_message: __("Generating PDFs..."),
          })
          .then(r => {
            const msg = r && r.message ? r.message : null;
            if (msg && msg.file_url) {
              frappe.show_alert({
                message: __("{0} reports merged. Download will start.", [msg.count || 0]),
                indicator: "green",
              });
              // open in new tab
              window.open(msg.file_url, "_blank");
            } else {
              frappe.msgprint({
                message: __("No file URL returned from the server."),
                indicator: "red",
              });
            }
          })
          .catch(e => {
            frappe.msgprint({
              message: __("Failed to generate PDF: {0}", [e.message || e]),
              indicator: "red",
            });
          })
          .always(() => {
            d.get_primary_btn().prop("disabled", false);
            d.set_primary_action(__("Generate"));
            d.hide();
          });
        },
      });

      d.show();
    });
  },
};
