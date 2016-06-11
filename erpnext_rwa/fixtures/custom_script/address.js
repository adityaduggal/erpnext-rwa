var read_only = ["address_line1", "address_line2", "city", "state", 
	"pincode", "country"];
	
var mandatory = ["block", "house_number", "floor"];

frappe.ui.form.on("Address", {
	onload: function(frm) {
		frm.set_query("house_number", function() {
			return {
				"filters": {
					"parent": frm.doc.block
				}
			};
		});
	},
	refresh: function(frm){
		resident(read_only, mandatory);
		non_resident(read_only, mandatory);
		title();
	}
});

cur_frm.cscript.block = function(doc, cdt, cdn){
	resident(read_only, mandatory);
	non_resident(read_only, mandatory);
	title();
}

cur_frm.cscript.house_number = function(doc, cdt, cdn){
	resident(read_only, mandatory);
	non_resident(read_only, mandatory);
	title();
}

cur_frm.cscript.floor = function(doc, cdt, cdn){
	resident(read_only, mandatory);
	non_resident(read_only, mandatory);
	title();
}

cur_frm.cscript.address_type = function(doc, cdt, cdn) {
	resident(read_only, mandatory);
	non_resident(read_only, mandatory);
	title();
}

function resident(read_only, mandatory){
	if (cur_frm.doc.address_type == "Resident"){
		cur_frm.set_value("address_line2", "Sunder Vihar");
		cur_frm.set_value("city", "New Delhi");
		cur_frm.set_value("state", "Delhi");
		cur_frm.set_value("pincode", "110087");
		cur_frm.set_value("country", "India");
		for (var i in read_only){
			cur_frm.set_df_property(read_only[i], "read_only", 1);
		}
		for (var i in mandatory){
			cur_frm.toggle_display(mandatory[i], true);
			cur_frm.toggle_reqd(mandatory[i], true);
		}
		if (null !== cur_frm.doc.block && null !== cur_frm.doc.house_number){
			cur_frm.set_value("address_line1", "Block# " + cur_frm.doc.block + ", House# " + cur_frm.doc.house_number + ", Floor: " + cur_frm.doc.floor)
		}
	}
}

function non_resident(read_only, mandatory){
	if (cur_frm.doc.address_type !== "Resident"){
		for (var i in read_only){
			cur_frm.set_df_property(read_only[i], "read_only", 0);
			cur_frm.set_value(read_only[i], null);
		}
		for (var i in mandatory){
			cur_frm.toggle_reqd(mandatory[i], false);
			cur_frm.toggle_display(mandatory[i], false);
			cur_frm.set_value(mandatory[i], null);
		}
	}
}

function title(){
	if (cur_frm.doc.address_type == "Resident"){
		cur_frm.set_value("address_title", cur_frm.doc.address_line1)
	}
	else{
		cur_frm.set_value("address_title", "")
	}
}

function disable_all(read_only, mandatory){
	for (var i in read_only){
		cur_frm.set_df_property(read_only[i], "read_only", 1);
	}
	for (var i in mandatory){
		cur_frm.set_df_property(mandatory[i], "read_only", 1);

	}
}