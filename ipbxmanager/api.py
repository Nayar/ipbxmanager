import frappe

@frappe.whitelist(allow_guest=True)
def domain_valid(domain):
	return True

@frappe.whitelist(allow_guest=True)
def add_company(domain, company_name, custom_domain,company_brn,contact_name,contact_email):
	if(custom_domain == 'no'):
		domain = domain + '.pbx.joolfoo.com'
	doc = frappe.get_doc({
		"doctype": "Freeswitch Domain",
		"company_name": company_name,
		"sip_domain" : domain,
		'company_brn' : company_brn,
		'contact_name' : contact_name,
		'contact_email': contact_email
	})
	doc.insert()
	return True
