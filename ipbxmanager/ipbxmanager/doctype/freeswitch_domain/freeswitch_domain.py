# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FreeswitchDomain(Document):
	def save(self):
		self.deploy()	
		super(FreeswitchDomain, self).save()
		
	def on_trash(self):
		import pprint
		pprint.pprint(self)
		for d in self.get_all_children():
			doc = frappe.get_doc(d.doctype,d.name)
			doc.delete()	
		
		#users = frappe.get_all('User', filters={'email': self.sip_email}, fields=['name'])
		sip_groups = frappe.get_all('SIP Group', filters={'freeswitch_domain': self.sip_domain}, fields=['name'])
		pprint.pprint(sip_groups)
		for sip_group in sip_groups:
			sip_group = frappe.get_doc("SIP Group",sip_group.name)
			sip_group.delete()
			
		sip_groups = frappe.get_all('SIP User', filters={'sip_domain': self.sip_domain}, fields=['name'])
		pprint.pprint(sip_groups)
		for sip_group in sip_groups:
			sip_group = frappe.get_doc("SIP User",sip_group.name)
			sip_group.delete()

		pprint.pprint('juju')
	
	def deploy(self):
		FreeswitchDomain.ansible_yaml_host_file()
		
	def ansible_yaml_host_file():
		import yaml,pprint,re
		
		obj = {
			"freeswitch": {
				"hosts" : {}
			},
			"bind": {
				"hosts": {}
			}			
		}
			
		dns_objs = []

		sip_servers = frappe.get_all('SIP Server')
		for sip_server in sip_servers:
			sip_server = frappe.get_doc('SIP Server',sip_server)
			obj['freeswitch']['hosts'][sip_server.ip] = { "domains" : [] }
			domains = frappe.get_all('Freeswitch Domain',filters={'sip_server': sip_server.name})
			for domain in domains:
				domain_obj = {
					"sip_domain" : domain.name,
					"users" : [],
					"groups" : []
				}
				
				domain = frappe.get_doc('Freeswitch Domain',domain)
				
				users = frappe.get_all('SIP User',filters={'sip_domain': domain.name})
				for user in users:
					user = frappe.get_doc('SIP User',user)
					domain_obj['users'].append({
						"sip_user_id": user.sip_user_id,
						"sip_password": user.sip_password
					})
					
				groups = frappe.get_all('SIP Group',filters={'sip_domain': domain.name})
				for group in groups:
					group = frappe.get_doc('SIP Group',group)
					group_obj = {
						"sip_extension" : group.sip_extension,
						"users" : []
					}
					for group_user in group.get_all_children():
						pprint.pprint(group_user)
						group_obj['users'].append(re.match("(.*)@.*",group_user.sip_user).group(1))
					domain_obj['groups'].append(group_obj)
				obj['freeswitch']['hosts'][sip_server.ip]['domains'].append(domain_obj)

				dns_objs.append({
					'name' : domain.name,
					'a' : sip_server.public_ip if sip_server.public_ip == '' else sip_server.ip
				})
				
		
		dns_servers = frappe.get_all('DNS Server')
		for dns_server in dns_servers:
			dns_server = frappe.get_doc('DNS Server',dns_server)
			obj['bind']['hosts'][dns_server.ip] = {
				"domains" : dns_objs
			}
		return yaml.dump(obj,default_flow_style=False)
