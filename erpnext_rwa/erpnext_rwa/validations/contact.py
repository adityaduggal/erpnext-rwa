# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import msgprint

def validate(doc,method):
	if doc.is_resident == 1 and (doc.address is None or doc.address == ""):
		frappe.throw("For Residents Address is Mandatory")
	elif doc.is_resident == 0 and doc.address:
		frappe.throw("Non-Resident Contacts cannot be linked to an Address")
	
	if doc.address:
		address = frappe.get_doc("Address", doc.address)
		if address.address_type <> "Resident":
			frappe.throw("Only Addresses belonging to Resident Category can be linked to Contacts")
	
	if doc.show_in_directory == 1 and doc.is_resident == 0:
		frappe.throw("Only Residents can opt for Show In Directory option")
		