# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import msgprint

def validate(doc,method):
	check_floor(doc,method)
	check_colony_placement(doc,method)
	
	#Change block as per the House Number
	user = frappe.session.user
	query = """SELECT role from `tabUserRole` where parent = '%s' """ %user
	roles = frappe.db.sql(query, as_list=1)
	
	if doc.address_type == "Resident":		
		doc.address_line1 = "Block# " + doc.block + ", House# " + \
			doc.house_number + ", Floor: " + doc.floor
		doc.address_line2 = "Sunder Vihar"
		doc.city = frappe.db.get_value("Block", doc.block, "city")
		doc.state = frappe.db.get_value("Block", doc.block, "state")
		doc.country = frappe.db.get_value("Block", doc.block, "country")
		doc.postal_code = frappe.db.get_value("Block", doc.block, "postal_code")


	if doc.address_type == "Resident" and doc.name <> doc.address_line1 \
		and not doc.get("__islocal"):
		if any("System Manager" in s  for s in roles):
			pass
		else:
			frappe.throw("Residential Address can only be Changed by System Manager")

def check_colony_placement(doc,method):
	user = frappe.session.user
	query = """SELECT role from `tabUserRole` where parent = '%s' """ %user
	roles = frappe.db.sql(query, as_list=1)
	
	if doc.address_type == "Resident":
		query = """SELECT colony_placement FROM `tabAddress`
			WHERE block = %s AND house_number = %s AND name <> '%s'""" %\
			(doc.block, doc.house_number, doc.name)
		same_address = frappe.db.sql(query, as_list=1)
		#frappe.throw(same_address)
		if same_address:
			if any(doc.colony_placement in s for s in same_address):
				pass
			else:
				if any("System Manager" in s  for s in roles):
					#If system admin changes the Colony Placement all houses are changed
					addresses = frappe.db.sql("""SELECT name FROM `tabAddress` WHERE block = %s 
						AND house_number = %s AND name <> '%s'""" % \
						(doc.block, doc.house_number, doc.name), as_list = 1)
					for i in addresses:
						frappe.db.set_value("Address", i[0], "colony_placement", doc.colony_placement)
				else:
					frappe.throw(("House Number: {0} cannot be {1} as already it has been \
						assigned other placement").format(doc.house_number, doc.colony_placement))
		
def check_floor(doc, method):
	#Checks FF can only be after GF, SF can only be after FF and TF can only be after SF
	if doc.address_type == "Resident":
		query = """SELECT floor FROM `tabAddress` 
			WHERE block = %s AND house_number = %s""" %(doc.block, doc.house_number)
		same_address = frappe.db.sql(query, as_list=1)
		if same_address:
			if doc.floor == "TF":
				if any("SF" in s for s in same_address):
					pass
				else:
					frappe.throw(("Third Floor (TF) not possible since there is no Second Floor (SF) \
						for House No: {0}.\n \
						If you want to Create a Third Floor (TF) Address First Create \
						Second Floor (SF) Address for House No: {1}").\
						format(doc.house_number, doc.house_number))
					
			elif doc.floor == "SF":
				if any("FF" in s for s in same_address):
					pass
				else:
					frappe.throw(("Second Floor (SF) not possible since there is no First Floor (FF) \
						for House No: {0}.\n \
						If you want to Create a Second Floor (SF) Address First Create \
						First Floor (FF) Address for House No: {1}").\
						format(doc.house_number, doc.house_number))
					
			elif doc.floor == "FF":
				if any("GF" in s for s in same_address):
					pass
				else:
					frappe.throw(("First Floor (FF) not possible since there is no Ground Floor (GF) \
						for House No: {0}.\n \
						If you want to Create a First Floor (FF) Address First Create \
						Ground Floor (GF) Address for House No: {1}").\
						format(doc.house_number, doc.house_number))
		else:
			if doc.floor <> "GF":
				frappe.throw(("Floor: {0} not possible since there is no Ground Floor (GF) \
					for House No: {1}.\n \
					If you want to Create a Floor: {2} for Address First Create \
					Ground Floor (GF) Address for House No: {2}").\
					format(doc.floor, doc.house_number, doc.floor, doc.house_number))
		
		
def autoname(doc,method):
	if doc.address_type == "Resident":
		house_block = frappe.db.sql("""SELECT parent FROM `tabHouse` 
			WHERE name = '%s'""" %doc.house_number, as_list=1)
		doc.block = house_block[0][0]
		doc.name = doc.address_type + ": " + doc.block + "/" + doc.house_number + ", " + doc.floor
	else:
		doc.name = doc.address_type + "-" + doc.address_title