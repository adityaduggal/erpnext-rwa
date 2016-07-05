// Copyright (c) 2016, Aditya Duggal and contributors
// For license information, please see license.txt

frappe.query_reports["Resident Directory"] = {
	"filters": [
		{
			"fieldname":"block",
			"label": "Block",
			"fieldtype": "Link",
			"options": "Block"
		},
		{
			"fieldname":"house",
			"label": "House Number",
			"fieldtype": "Link",
			"options": "House"
		},
		{
			"fieldname":"floor",
			"label": "Floor",
			"fieldtype": "Select",
			"options": "\nGF\nFF\nSF\nTF"
		},
	]
}
