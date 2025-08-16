// Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Breakfast"] = {
    filters: [
        {
            fieldname: "username",
            label: __("Name"),
            fieldtype: "data",
            options: "employee",
            reqd: 1,
            default: frappe.defaults.get_user_default("Employee"),
        },
    ],
};
