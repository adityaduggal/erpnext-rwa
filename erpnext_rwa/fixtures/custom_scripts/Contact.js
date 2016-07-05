frappe.ui.form.on("Contact", {
	refresh: function(frm) {
		frm.events.show_message(frm);
	},
	
	onload: function(frm){
		frm.set_query("address", function() {
			return {
				"filters": {
					"address_type": "Resident",
				}
			};
		});
	},
	show_message: function(frm) {
	frm.dashboard.reset();
	frm.dashboard.set_headline_alert('Make a Contact as Resident only after attaching the \
		Address Proof of the Resident');
	},
});

cur_frm.cscript.is_resident = function(doc, cdt, cdn) {
	cur_frm.toggle_reqd("address", false);
};