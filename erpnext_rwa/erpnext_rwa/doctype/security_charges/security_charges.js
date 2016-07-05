// Copyright (c) 2016, Aditya Duggal and contributors
// For license information, please see license.txt

frappe.ui.form.on('Security Charges', {
	refresh: function(frm) {
	},
	
	onload: function(frm){
		frm.set_query("received_from", function() {
			return {
				"filters": {
					"is_resident": 1,
				}
			};
		});
	},

	show_message: function(frm) {
	frm.dashboard.reset();
	frm.dashboard.set_headline_alert('1. Security Charges are based on Monthly Values \n \
		2. Security Charges are possible per address per period once only');
	},
	
});

frappe.ui.form.on('Security Charges', "number_of_months", function(frm, cdt, cdn){
	var d = locals[cdt][cdn]
	frappe.model.set_value(cdt, cdn, "total_amount", d.number_of_months * d.rate_per_month);
	cur_frm.refresh_fields();
});

frappe.ui.form.on('Security Charges', "rate_per_month", function(frm, cdt, cdn){
	var d = locals[cdt][cdn]
	frappe.model.set_value(cdt, cdn, "total_amount", d.number_of_months * d.rate_per_month);
	cur_frm.refresh_fields();
});