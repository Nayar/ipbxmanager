# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FreeswitchDomain(Document):
	def deploy(self):
		import base64
		import paramiko
		print("Deploying...")

		key = paramiko.RSAKey.from_private_key_file("/home/frappe/.ssh/id_rsa")
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect('10.65.35.52', username='root')
		stdin, stdout, stderr = client.exec_command('mkdir -p /etc/freeswitch/directory/' + self.sip_domain)
		for line in stdout:
			print('... ' + line.strip('\n'))
		for line in stderr:
			print('... ' + line.strip('\n'))
		client.close()
		self.deploy_sip_users()
		pass
	
	def deploy_sip_users(self):
		users=frappe.get_all('SIP User', filters={'sip_domain': self.sip_domain}, fields=['name','sip_user_id'])
		for user in users:
			print(user)
		print('wowo')
		
	def save(self):
		import pprint
		#pprint.pprint(vars(self))
		for d in self.get_all_children():
			if(d.doctype == 'SIP User Child'):
				if not frappe.db.exists("SIP User", d.sip_user_id + '@' + self.sip_domain):
					doc = frappe.get_doc({
						"doctype": "SIP User",
						"sip_user_id" : d.sip_user_id,
						"sip_domain" : self.sip_domain,
						"sip_email" : d.sip_user_id + '@' + self.sip_domain
					})
					doc.insert()
				d.sip_user = d.sip_user_id + '@' + self.sip_domain
				
			if(d.doctype == 'SIP Group Child'):
				if not frappe.db.exists("SIP Group", self.sip_domain + '-' + d.sip_group_extension):
					doc = frappe.get_doc({
						"doctype": "SIP Group",
						"sip_extension": str(d.sip_group_extension),
						"freeswitch_domain" : self.sip_domain
					})
					doc.insert()
				d.sip_group = self.sip_domain + '-' + d.sip_group_extension
		super(FreeswitchDomain, self).save()
		self.deploy()
		
