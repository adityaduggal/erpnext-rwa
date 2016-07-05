# Copyright (c) 2013, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data
	
def get_columns(filters):
	return [
		"Security Charges:Link/Security Charges:100", "Contact:Link/Contact:180", "Address:Link/Address:200",
		"From Date:Date:80", "To Date:Date:80", "Period:Int:50", "Monthly Charge:Currency:100",
		"Total Amount:Currency:100", "Block:Int:50", "House:Int:50", "Floor::50", "Received By:Link/Contact:100"
		]
	
def get_data (filters):
	conditions_add, conditions_sec = get_conditions(filters)
	query = """SELECT sec.name, sec.received_from, sec.address, sec.posting_date,
		sec.period_to, sec.number_of_months, sec.rate_per_month, sec.total_amount,
		ad.block, ad.house_number, ad.floor, sec.received_by
		
		FROM `tabSecurity Charges` sec, `tabAddress` ad
		
		WHERE 
			sec.docstatus = 1 AND
			sec.address = ad.name %s %s
			
		ORDER BY sec.posting_date, ad.block, ad.house_number, ad.floor""" \
		%(conditions_add, conditions_sec)
	data = frappe.db.sql(query, as_list = 1)
	
	return data
	
def get_conditions(filters):
	conditions_add = ""
	conditions_sec = ""
	
	if filters.get("from_date"):
		conditions_sec += " AND sec.posting_date <= '%s'" % filters["from_date"]
	
	if filters.get("to_date"):
		conditions_sec += " AND sec.period_to <= '%s'" % filters["to_date"]

	if filters.get("payment_receipt_date"):
		conditions_sec += " AND sec.payment_receipt_date = '%s'" % filters["payment_receipt_date"]
		
	if filters.get("block"):
		conditions_add += " AND ad.block = '%s'" % filters["block"]
		
	if filters.get("house"):
		conditions_add += " AND ad.house_number = '%s'" % filters["house"]
		
	return conditions_add, conditions_sec
