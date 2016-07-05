# -*- coding: utf-8 -*-
# Copyright (c) 2015, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import calendar
from datetime import datetime, timedelta
from frappe.model.document import Document
from frappe.utils import getdate, cint, add_months, date_diff, add_days, nowdate, \
	get_datetime_str, cstr, get_datetime, time_diff, time_diff_in_seconds

class SecurityCharges(Document):
	#Rules
	#1. One house cannot have multiple charges for same period_to
	#2. Maximum limit to number of months is 12 (hardcoded)
	#3. Start Date should be from Begining of a MONTH
	def validate(self):
		self.validate_dates()
		self.validate_address()
	

	def validate_address(self):
		recd_from = frappe.get_doc("Contact", self.received_from)
		if recd_from.is_resident <> 1:
			frappe.throw("Security Deposit Only allowed from Residents")
		#Check if Resident's Address has already been paid for Period maybe from another contact
		overlapping_sc = frappe.db.sql("""SELECT sc.name FROM `tabSecurity Charges` sc 
			WHERE 
			sc.docstatus = 1 AND sc.address = '%s' AND 
			((sc.posting_date <= '%s' AND sc.period_to >= '%s') OR 
			(sc.posting_date <= '%s' AND sc.period_to >= '%s'))""" 
			%(self.address, self.posting_date, self.posting_date, \
			self.period_to, self.period_to), as_list=1)

			
		if overlapping_sc:
			frappe.throw(("There are existing Security Charges Entry \n \
			For Address {0} and hence this entry cannot be Created \n \
			Please check the Security Charges for this Address").format(self.address))
		
		
	
	def validate_dates(self):
		if self.number_of_months > 12:
			frappe.throw("Maximum Allowed Security Charges are for 12 Months Only")
		self.address = frappe.get_value("Contact", self.received_from, "address")
		month = getdate(self.posting_date).month
		year = getdate(self.posting_date).year
		new_date = str(year) + str(month) + str(01)
		self.posting_date = datetime.strptime(new_date, "%Y%m%d").date()
		date = getdate(self.posting_date)
		upto_date = add_months(date,self.number_of_months-1)
		last_date = calendar.monthrange(upto_date.year, upto_date.month)[1]
		upto_date = datetime.strptime(str(upto_date.year)+str(upto_date.month)+str(last_date), "%Y%m%d").date()
		self.period_to = upto_date
		self.total_amount = self.number_of_months * self.rate_per_month
