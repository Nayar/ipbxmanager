# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import pprint
from ipbxmanager.api import *

class SIPUser(Document):
	def validate(self):
		#company = frappe.get_doc("Company",self.company)
		#self.name = self.sip_user_id + '@' + company.domain
		pass

	def on_update(self):
		#try:
			#doc = frappe.get_doc({
				#"doctype": "User",
				#"email" : self.sip_email,
				#"first_name" : self.sip_user_id,
				#"last_name" : self.sip_domain,
				#"new_password" : '1234a@A!'
			#})
		
			#doc.insert()
		#except e:
			#print('exception in create user')
		#deploy()
		pass

	def on_trash(self):
		#users = frappe.get_all('User', filters={'email': 'self.sip_email'}, fields=['name'])
		#print('juju')
		#pprint.pprint(users)
		#print('juju')
		#user = frappe.get_doc("User",self.name)
		#contact = frappe.get_doc("Contact",user.full_name)
		#contact.delete()
		#user.delete()
		#deploy()
		pass


