// Copyright (c) 2018, Nayar Joolfoo and contributors
// For license information, please see license.txt

frappe.ui.form.on('SIP Group', {
	onload: function(frm) {
		console.log(frm)
		
		frm.set_query("sip_user", "sip_users", function(doc) {
			return { "filters" : {
				'sip_domain' : doc.freeswitch_domain
			}}
		});
	},
});
