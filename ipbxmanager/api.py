import frappe
import pprint
from ipbxmanager.ipbxmanager.doctype.freeswitch_domain.freeswitch_domain import *

fields_company = ['name','company_name','company_brn','contact_name','contact_email','contact_tel','limit_sip_groups','limit_sip_users']
fields_users = ['name','sip_user_id']

@frappe.whitelist(allow_guest=True)
def domain_valid(domain):
	return True

@frappe.whitelist(allow_guest=True)
def add_company(domain, company_name, custom_domain,company_brn,contact_name,contact_email,contact_position,company_website):
	if(custom_domain == 'no'):
		domain = domain + '.pbx.joolfoo.com'
	doc = frappe.get_doc({
		"doctype": "Freeswitch Domain",
		"company_name": company_name,
		"sip_domain" : domain,
		'company_brn' : company_brn,
		'contact_name' : contact_name,
		'contact_email': contact_email,
		'contact_position' : contact_position,
		'company_website' : company_website
	})
	doc.insert(ignore_permissions=True)
	return True

@frappe.whitelist(allow_guest=True)
def add_group(sip_domain, group_name, sip_extension):
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user, 'name': sip_domain}, fields=fields_company)
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'name': sip_domain}, fields=fields_company)
	if(len(sip_domains) >= 1):
		doc = frappe.get_doc({
			"doctype": "SIP Group",
			"sip_extension": sip_extension,
			"group_name": group_name,
			"sip_domain": sip_domain
		})
		return doc.insert(ignore_permissions=True)
	return False

@frappe.whitelist(allow_guest=True)
def add_users(sip_domain, start_uid, end_uid):
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user, 'name': sip_domain}, fields=fields_company)
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'name': sip_domain}, fields=fields_company)
	if(len(sip_domains) >= 1):
		arr = []
		start_uid = int(start_uid)
		end_uid = int(end_uid) + 1
		for uid in range(start_uid,end_uid):
			doc = frappe.get_doc({
				"doctype": "SIP User",
				"sip_user_id": uid,
				"sip_domain": sip_domain,
				"sip_email": str(uid) + '@' + sip_domain
			})
			pprint.pprint(doc)
			arr.append(doc)
			doc.insert(ignore_permissions=True)
		return arr
	return False

@frappe.whitelist(allow_guest=True)
def get_companies():
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user}, fields=fields_company)
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={}, fields=fields_company)
	return sip_domains

@frappe.whitelist(allow_guest=True)
def get_company(company_name):
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user, 'name': company_name}, fields=fields_company)
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'name': company_name}, fields=fields_company)
	pprint.pprint(sip_domains)
	return sip_domains[0]

@frappe.whitelist(allow_guest=True)
def get_users(company_name):
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user, 'name': company_name}, fields=fields_company)
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'name': company_name}, fields=fields_company)
	print(sip_domains)
	print(len(sip_domains))
	if(len(sip_domains) >= 1):
		sip_users = frappe.get_all('SIP User', filters={'sip_domain': company_name}, fields=fields_users)
		return sip_users
	return []

@frappe.whitelist(allow_guest=True)
def get_groups(company_name):
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user, 'name': company_name}, fields=fields_company)
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'name': company_name}, fields=fields_company)
	print(sip_domains)
	print(len(sip_domains))
	if(len(sip_domains) >= 1):
		sip_users = frappe.get_all('SIP Group', filters={'sip_domain': company_name}, fields=['name','group_name','sip_extension'])
		return sip_users
	return []

@frappe.whitelist(allow_guest=True)
def delete_sip_user(company_name,sip_user):
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user, 'name': company_name}, fields=fields_company)
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'name': company_name}, fields=fields_company)
	if(len(sip_domains) >= 1):
		user = frappe.delete_doc('SIP User', sip_user,ignore_permissions=True)
		frappe.db.commit()
	return True

@frappe.whitelist(allow_guest=True)
def delete_sip_group(company_name,sip_group):
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user, 'name': company_name}, fields=fields_company)
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'name': company_name}, fields=fields_company)
	if(len(sip_domains) >= 1):
		user = frappe.delete_doc('SIP Group', sip_group,ignore_permissions=True)
		frappe.db.commit()
	return True

@frappe.whitelist(allow_guest=True)
def current_user():
	return frappe.session.user

@frappe.whitelist(allow_guest=True)
def deploy():
	FreeswitchDomain.deploy()
