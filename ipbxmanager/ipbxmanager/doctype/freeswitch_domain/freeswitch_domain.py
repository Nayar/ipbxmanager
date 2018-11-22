# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FreeswitchDomain(Document):
	def save(self):
		import pprint
		pprint.pprint(vars(self))

		for d in self.get_all_children():
			if(d.doctype != 'SIP User'):
				continue
			pprint.pprint(vars(d))
			print(d.sip_user_id)
			print(self.sip_domain)
			d.sip_email = d.sip_user_id + '@' + self.sip_domain
		super(FreeswitchDomain, self).save()
