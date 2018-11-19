# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SIPUser(Document):
    def validate(self):
        company = frappe.get_doc("Company",self.company)
        self.name = self.sip_user_id + '@' + company.domain

    def on_update(self):
        company = frappe.get_doc("Company",self.company)
        doc = frappe.get_doc({
            "doctype": "User",
            "email" : self.name,
            "first_name" : self.sip_user_id,
            "last_name" : company.domain
        })
        doc.insert()

    def on_trash(self):
        user = frappe.get_doc("User",self.name)
        contact = frappe.get_doc("Contact",user.full_name)
        contact.delete()
        user.delete()



