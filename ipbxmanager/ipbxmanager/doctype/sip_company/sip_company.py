# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import pprint

class SIPCompany(Document):
    
    def save(self):
        for d in self.get_all_children():
            d.sip_email = d.sip_user_id + '@' + self.sip_domain
        super(SIPCompany, self).save()
        
                
    def on_update(self):
        company = self
        pprint.pprint(vars(self))
        print('here')
        for user in self.sip_users:
            user.sip_email = user.sip_user_id + '@' + company.sip_domain
            if not frappe.db.exists("User", user.sip_user_id + '@' + company.sip_domain):
                doc = frappe.get_doc({
                    "doctype": "User",
                    "email" : user.sip_user_id + '@' + company.sip_domain,
                    "first_name" : user.sip_user_id,
                    "last_name" : company.sip_domain,
                    "new_password" : '1234a@A!'
                })
                doc.insert()
                
                

