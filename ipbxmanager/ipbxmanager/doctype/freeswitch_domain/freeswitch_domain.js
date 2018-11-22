// Copyright (c) 2018, Nayar Joolfoo and contributors
// For license information, please see license.txt
var i = 1;
frappe.ui.form.on('Freeswitch Domain', {
	refresh: function(frm) {
        frm.add_custom_button(__("Generate Users"), function(){
            console.log(frappe)
            console.log(frm)

            var newrow = frappe.model.add_child(frm.doc, "SIP User", "sip_users");
            newrow.sip_user_id = String(100 + i++)

            frm.refresh()
        });
	}
});
