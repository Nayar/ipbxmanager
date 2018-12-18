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
	sip_domains=frappe.get_all('Freeswitch Domain', filters={'contact_email': frappe.session.user}, fields=['name','company_name','contact_name'])
	return sip_domains

@frappe.whitelist(allow_guest=True)
def current_user():
	return frappe.session.user
