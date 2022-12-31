# Copyright (c) 2021, John and contributors
# For license information, please see license.txt

# import frappe
import re
import frappe
from frappe.model.document import Document

class CreditCheck(Document):
	def before_save(self):
		self.country_code = self.country_code.upper()
		self.bzno = re.sub("\-", "",  self.bzno)
		self.name =  self.country_code.upper() + "-" + re.sub("\-", "",  self.bzno)
	def after_insert(self):
		# print(self.customer)
		if self.customer:
			frappe.db.set_value("Customer",self.customer,"credit_check",self.name)
			# customer_doc = frappe.get_doc("Customer",self.customer)
			# customer_doc.db_set('credit_check', self.name)
			# customer_doc.save()
		

@frappe.whitelist()
def make_credit_rate(doctype, docname):
	doc = frappe.new_doc("Credit Check")
	customer_doc = frappe.get_doc(doctype,docname)
	doc.country = customer_doc.country
	doc.country_code = customer_doc.country_code
	doc.bzno = customer_doc.tax_id
	doc.bzno = customer_doc.tax_id
	doc.enp_nm = customer_doc.customer_name
	doc.customer = docname
	# doc.set(frappe.scrub(doctype), docname)
	# doc.selling = 1 if doctype == "Customer" else 0
	# doc.buying = 1 if doctype == "Supplier" else 0

	return doc


