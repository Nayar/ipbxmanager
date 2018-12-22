import frappe

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
	doc.insert()
	return True

@frappe.whitelist(allow_guest=True)
def get_companies():
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user}, fields=['name','company_name','company_brn'])
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={}, fields=['name','company_name','company_brn'])
	return sip_domains

@frappe.whitelist(allow_guest=True)
def get_company(company_name):
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user, 'name': company_name}, fields=['name','company_name','company_brn'])
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'name': company_name}, fields=['name','company_name','company_brn'])
	return sip_domains[0]

@frappe.whitelist(allow_guest=True)
def get_users(company_name):
	if(frappe.session.user != 'Administrator'):
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user, 'name': company_name}, fields=['name','company_name','company_brn'])
	else:
		sip_domains=frappe.get_all('Freeswitch Domain', filters={'name': company_name}, fields=['name','company_name','company_brn'])
	print(sip_domains)
	print(len(sip_domains))
	if(len(sip_domains) >= 1):
		sip_users = frappe.get_all('SIP User', filters={'sip_domain': company_name}, fields=['sip_user_id'])
		return sip_users
	return []

@frappe.whitelist(allow_guest=True)
def current_user():
	return frappe.session.user
