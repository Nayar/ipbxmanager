import frappe

@frappe.whitelist(allow_guest=True)
def domain_valid(domain):
	return True

@frappe.whitelist()
def add_company(domain, company_name, custom_domain):
	if(custom_domain == 'no'):
		domain = domain + '.pbx.joolfoo.com'
	doc = frappe.get_doc({
		"doctype": "Freeswitch Domain",
		"company_name": company_name,
		"sip_domain" : domain
	})
	doc.insert()
	return True
