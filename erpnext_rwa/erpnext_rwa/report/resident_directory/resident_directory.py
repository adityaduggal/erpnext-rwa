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
		"Block:Int:50", "House Number:Int:80", "Floor::50", "First Name::100",
		"Last Name::100", "Mobile Number::150", "Phone Number::150", "Email ID::200"
	]

def get_data(filters):
	conditions_add = get_conditions(filters)
	query = """SELECT ad.block, ad.house_number, 
	ad.floor, co.first_name, co.last_name, 
	co.mobile_no, co.phone, co.email_id
	FROM `tabContact` co, `tabAddress` ad
	WHERE
		co.show_in_directory = 1 AND
		ad.name = co.address %s
	ORDER BY
		CAST(ad.block AS UNSIGNED), CAST(ad.house_number AS UNSIGNED),
		ad.floor, co.first_name""" %conditions_add
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