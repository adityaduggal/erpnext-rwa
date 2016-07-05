# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import msgprint

def validate(doc,method):
	#Change block as per the House Number
	if doc.address_type == "Resident":		
		doc.address_line1 = "Block# " + doc.block + ", House# " + \
			doc.house_number + ", Floor: " + doc.floor
		doc.address_line2 = "Sunder Vihar"
		doc.city = frappe.db.get_value("Block", doc.block, "city")
		doc.state = frappe.db.get_value("Block", doc.block, "state")
		doc.country = frappe.db.get_value("Block", doc.block, "country")
		doc.postal_code = frappe.db.get_value("Block", doc.block, "postal_code")


	if doc.address_type == "Resident" and doc.name <> doc.address_line1 and not doc.get("__islocal"):
		frappe.throw("Residential Address not Allowed to be Changed")
	#elif doc.name[:7] <> "Outside":
		#frappe.throw("Outside Address cannot be changed to Residential Address")

def autoname(doc,method):
	if doc.address_type == "Resident":
		house_block = frappe.db.sql("""SELECT parent FROM `tabHouse` 
			WHERE name = '%s'""" %doc.house_number, as_list=1)
		doc.block = house_block[0][0]
		doc.name = doc.address_type + ": " + doc.block + "/" + doc.house_number + ", " + doc.floor
	else:
		doc.name = doc.address_type + "-" + doc.address_title