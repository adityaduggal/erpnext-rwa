# Copyright (c) 2013, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data
	
def get_columns():
	return [
		"Address:Link/Address:120", "Block:Int:40", "House Number:Int:40", "Floor::40", "First Name::80",
		"Last Name::80", "Mobile Number::150", "Phone Number::150", "Email ID::200", 
		"Contact:Link/Contact:150"
	]

def get_data(filters):
	conditions_add = get_conditions(filters)
	query = """SELECT ad.name, ad.block, ad.house_number, 
	ad.floor, IFNULL(co.first_name, "-"), IFNULL(co.last_name, "-"),
	IFNULL(co.mobile_no, "-"), IFNULL(co.phone, "-"), IFNULL(co.email_id, "-"),
	IFNULL(co.name, "-")
	FROM `tabAddress` ad
		LEFT JOIN `tabContact` co ON ad.name = co.address AND co.show_in_directory = 1
	WHERE
		ad.address_type = 'Resident' %s
	ORDER BY
		CAST(ad.block AS UNSIGNED), CAST(ad.house_number AS UNSIGNED),
		ad.floor""" % conditions_add
	data = frappe.db.sql(query, as_list =1)
	return data
	
def get_conditions(filters):
	conditions_add = ""

	if filters.get("block"):
		conditions_add += " AND ad.block = '%s'" % filters["block"]

	if filters.get("house"):
		conditions_add += " AND ad.house_number = '%s'" % filters["house"]
		
	if filters.get("floor"):
		conditions_add += " AND ad.floor = '%s'" % filters["floor"]
	return conditions_add