# Copyright (c) 2021, John and contributors
# For license information, please see license.txt

# import frappe
import re
from frappe.model.document import Document

class CreditCheck(Document):
	def before_save(self):
		self.country_code = self.country_code.upper()
		self.bzno = re.sub("\-", "",  self.bzno)
		self.name =  self.country_code.upper() + "-" + re.sub("\-", "",  self.bzno)


