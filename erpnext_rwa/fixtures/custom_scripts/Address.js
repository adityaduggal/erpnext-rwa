var general_fields = ["address_line1", "address_line2", "city", "state", 
	"pincode", "country"];
	
var specific_fields = ["block", "house_number", "floor"];
var others = ["address_title"]
var add_type = ["address_type"]
var extra = ["email_id", "phone", "fax", "linked_with", "is_primary_address", "is_shipping_address", "county", "test"]

frappe.ui.form.on("Address", {
	refresh: function(frm){
		if (frm.doc.__islocal) {
			if (cur_frm.doc.address_type == "Resident"){
				
				read_only(general_fields);
				read_only(specific_fields);
				read_only(others);
				read_only(add_type);
				hide_fields(extra);
			}
			else {
				make_all_editable();
				hide_fields(extra);
				hide_fields(specific_fields);
			}
		}
		else{
			if (cur_frm.doc.address_type == "Resident") {
				read_only(general_fields);
				read_only(specific_fields);
				read_only(others);
				read_only(add_type);
				hide_fields(extra);
			}
		}
	},
	
	onload: function(frm){
		frm.set_query("house_number", function() {
			return {
				"filters": {
					"parent": cur_frm.doc.block,
				}
			};
		});
	},
});

cur_frm.cscript.address_type = function(doc, cdt, cdn) {
	if (cur_frm.doc.address_type == "Outside"){
		cur_frm.doc.address_title = ""
		cur_frm.doc.block = ""
		cur_frm.doc.house_number = ""
		cur_frm.doc.floor = ""
		unhide_all_fields();
		remove_all_mandatory();
		make_all_editable();
		hide_fields(extra);
		hide_fields(specific_fields);
		make_mandatory(general_fields);
	}
	else {
		cur_frm.doc.address_title = "Resident"
		cur_frm.doc.block = ""
		cur_frm.doc.house_number = ""
		cur_frm.doc.floor = ""
		unhide_all_fields();
		remove_all_mandatory();
		make_all_editable();
		read_only(general_fields);
		//read_only(specific_fields);
		read_only(others);
		hide_fields(extra);
		make_mandatory(specific_fields);
	}
};


/*
Below are the functions which are used to hide/unhide/mandatory/read_only etc
*/

function hide_fields(list){
	for (var i in list){
		cur_frm.toggle_display(list[i], false);
	}
}

function show_fields(list){
	for (var i in list){
		cur_frm.toggle_display(list[i], true);
	}
}

function make_mandatory(list){
	for (var i in list){
		cur_frm.toggle_reqd(list[i], true);
	}
}

function remove_mandatory(list){
	for (var i in list){
		cur_frm.toggle_reqd(list[i], false);
	}
}

function read_only(list){
	for (var i in list){
		cur_frm.set_df_property(list[i], "read_only", 1);
	}
}

function editable(list){
	for (var i in list){
		cur_frm.set_df_property(list[i], "read_only", 0);
	}
}

function make_all_editable(){
	editable(general_fields);
	editable(specific_fields);
	editable(others);
	editable(extra);
}

function unhide_all_fields(){
	show_fields(general_fields);
	show_fields(specific_fields);
	show_fields(others);
	show_fields(extra);
}

function remove_all_mandatory(){
	remove_mandatory(general_fields);
	remove_mandatory(specific_fields);
	remove_mandatory(extra);	
}