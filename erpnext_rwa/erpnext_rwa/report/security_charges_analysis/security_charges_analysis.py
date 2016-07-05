# Copyright (c) 2013, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	
	return columns, data
	
def get_columns(filters):
	if filters.get("unpaid") <> 1:
		return [
			"Security Charges:Link/Security Charges:80", "Received From:Link/Contact:100", 
			"Address:Link/Address:150",
			"From Date:Date:80", "To Date:Date:80", "Period:Int:50", "Monthly Charge:Currency:100",
			"Total Amount:Currency:100", "Block:Int:50", "House:Int:50", "Floor::50", 
			"Received By:Link/Contact:100", "Payment Receipt Date:Date:80"		
			]
	else:
		return[
			"Address:Link/Address:150", "Block:Int:50", "House:Int:50", "Floor::50"
		]
	
def get_data (filters):
	conditions_add, conditions_sec = get_conditions(filters)
	if filters.get("unpaid") <> 1:
		query = """SELECT sec.name, sec.received_from, sec.address, sec.posting_date,
			sec.period_to, sec.number_of_months, sec.rate_per_month, sec.total_amount,
			ad.block, ad.house_number, ad.floor, sec.received_by, sec.payment_receipt_date
			
			FROM `tabSecurity Charges` sec, `tabAddress` ad
			
			WHERE 
				sec.docstatus = 1 AND
				sec.address = ad.name %s %s
				
			ORDER BY sec.posting_date, ad.block, ad.house_number, ad.floor""" \
			%(conditions_add, conditions_sec)
	else:
		query = """SELECT ad.name, ad.block, ad.house_number, ad.floor
			
			FROM `tabAddress` ad
			
			WHERE ad.address_type = 'Resident' %s AND ad.name NOT IN (
				SELECT ad.name FROM `tabSecurity Charges` sec
				WHERE ad.name = sec.address AND sec.docstatus = 1 %s)
			
			ORDER BY
				CAST(ad.block AS UNSIGNED), CAST(ad.house_number AS UNSIGNED), ad.floor""" \
				%(conditions_add, conditions_sec)
	data = frappe.db.sql(query, as_list = 1)
	
	return data
	
def get_conditions(filters):
	conditions_add = ""
	conditions_sec = ""
	
	if filters.get("from_date"):
		conditions_sec += " AND (sec.posting_date <= '%s' OR \
			sec.period_to >= '%s')" % (filters["from_date"],filters["from_date"])
	
	if filters.get("to_date"):
		conditions_sec += " AND (sec.period_to <= '%s' OR sec.posting_date <= '%s')" % (filters["to_date"],filters["to_date"])

	if filters.get("payment_receipt_date"):
		conditions_sec += " AND sec.payment_receipt_date = '%s'" % filters["payment_receipt_date"]
		
	if filters.get("block"):
		conditions_add += " AND ad.block = '%s'" % filters["block"]
		
	if filters.get("house"):
		conditions_add += " AND ad.house_number = '%s'" % filters["house"]
		
	return conditions_add, conditions_sec
