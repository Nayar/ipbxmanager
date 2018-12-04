# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

def gen_user_xml(domain,i):
	return """<include>
<user id="%s">
	<params>
	<param name="reverse-auth-user" value="%s" />
	<param name="reverse-auth-pass" value="12034" />
	</params>
</user>
</include>""" % (i,i)

class FreeswitchDomain(Document):
  
	def ssh_command(self,cmd):
		import base64
		import paramiko
		sip_server = frappe.get_doc('SIP Server', self.sip_server)
		key = paramiko.RSAKey.from_private_key_file("/home/frappe/.ssh/id_rsa")
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(sip_server.ip, username='root')
		stdin, stdout, stderr = client.exec_command(cmd)
		client.close()
		return stdin, stdout, stderr
  
	def deploy(self):

		print("Deploying..." + self.sip_domain)
		stdin, stdout, stderr = self.ssh_command('rm -rf /etc/freeswitch/directory/' + self.sip_domain)
		stdin, stdout, stderr = self.ssh_command('mkdir -p /etc/freeswitch/directory/' + self.sip_domain)
		for line in stdout:
			print('... ' + line.strip('\n'))
		for line in stderr:
			print('... ' + line.strip('\n'))
		self.deploy_sip_users()
		self.ssh_command('systemctl restart freeswitch')
		pass
	
	def deploy_sip_users(self):
		users=frappe.get_all('SIP User', filters={'sip_domain': self.sip_domain}, fields=['name','sip_user_id'])
		for user in users:
			print(user)
			stdin, stdout, stderr = self.ssh_command("echo '" + gen_user_xml(self.sip_domain,user.sip_user_id) + "' > /etc/freeswitch/directory/%s/%s.xml " % (self.sip_domain,user.sip_user_id))
			for line in stdout:
				print('... ' + line.strip('\n'))
			for line in stderr:
				print('... ' + line.strip('\n'))
			
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
		sip_server = frappe.get_doc('SIP Server', self.sip_server)
		A = sip_server.ip
		if(sip_server.ip_public != None and sip_server.ip_public != ''):
			A = sip_server.ip_public
			
		
		dns_servers=frappe.get_all('DNS Server')
		for server in dns_servers:
			dns_server = frappe.get_doc('DNS Server', server.name)
			dns_server.add_domain(self.sip_domain,A)
		
