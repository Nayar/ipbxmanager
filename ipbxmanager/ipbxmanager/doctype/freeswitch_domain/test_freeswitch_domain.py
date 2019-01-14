# -*- coding: utf-8 -*-
# Copyright (c) 2018, Nayar Joolfoo and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from ipbxmanager.ipbxmanager.doctype.freeswitch_domain.freeswitch_domain import *

class TestFreeswitchDomain(unittest.TestCase):
	def test_yaml_host_file(self):
		print(FreeswitchDomain.ansible_yaml_host_file())
