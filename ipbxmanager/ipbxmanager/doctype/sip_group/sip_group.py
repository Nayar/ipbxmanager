# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from ipbxmanager.api import *

class SIPGroup(Document):
	def on_update(self):
		#deploy()
		pass

	def on_trash(self):
		#deploy()
		pass
