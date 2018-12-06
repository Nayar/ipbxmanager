# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document



class DNSServer(Document):
	def ssh_command(self,cmd):
		import base64
		import paramiko
		key = paramiko.RSAKey.from_private_key_file("/home/frappe/.ssh/id_rsa")
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(self.ip, username='root')
		stdin, stdout, stderr = client.exec_command(cmd)
		client.close()
		return stdin, stdout, stderr
	
	def add_domain(self,domain,A):
		zone_str = """zone "%s" { 
type master; 
file "/etc/bind/zones/%s.db"; 
};""" % (domain,domain)

		zone_data = """$TTL 14400
@ IN SOA ns1.joolfoo.com webmaster.joolfoo.com. (
201006601 ; Serial
7200 ; Refresh
120 ; Retry
2419200 ; Expire
604800) ; Default TTL
;


%s. IN A %s
@ IN NS ns1.%s.
ns1 IN A %s""" % (domain,domain,A,domain,self.ip)
		stdin, stdout, stderr = self.ssh_command("echo '" + zone_str + "' > /etc/bind/named.conf.local")
		stdin, stdout, stderr = self.ssh_command("echo '%s' > /etc/bind/zones/%s.db" % (zone_data,domain))
		stdin, stdout, stderr = self.ssh_command("systemctl restart bind9 2>&1")
		for line in stdout:
			print('... ' + line.strip('\n'))
		for line in stderr:
			print('... ' + line.strip('\n'))
		print('kkkkkkkk')
