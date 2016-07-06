// Copyright (c) 2016, Aditya Duggal and contributors
// For license information, please see license.txt

frappe.query_reports["Security Charges Analysis"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": "Security From Date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -3),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": "Security Upto Date",
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 0
		},
		{
			"fieldname":"block",
			"label": "Block",
			"fieldtype": "Link",
			"option": "Block"
		},
		{
			"fieldname":"house",
			"label": "House Number",
			"fieldtype": "Link",
			"option": "House"
		},
		{
			"fieldname":"placement",
			"label": "House Placement",
			"fieldtype": "Select",
			"options": "\nInside\nOutside"
		},
		{
			"fieldname":"payment_receipt_date",
			"label": "Payment Receipt Date",
			"fieldtype": "Date"
		},
		{
			"fieldname":"unpaid",
			"label": "Show Unpaid",
			"fieldtype": "Check"
		},
	]
}
