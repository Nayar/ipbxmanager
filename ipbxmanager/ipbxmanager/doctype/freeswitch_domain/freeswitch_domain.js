// Copyright (c) 2018, Nayar Joolfoo and contributors
// For license information, please see license.txt
var i = 1;
frappe.ui.form.on('Freeswitch Domain', {
	refresh: function(frm) {
        frm.add_custom_button(__("Generate Users"), function(){
            console.log(frappe)
            console.log(frm)
            frappe.prompt([
                    {'fieldname': 'no_of_users_to_generate', 'fieldtype': 'Int', 'label': 'No of users to generate', 'reqd': 1}  
                ],
                function(values){
                    show_alert(values, 5);
                    console.log(values)
                    for(var i = 0; i < values.no_of_users_to_generate ; i++){
                        var newrow = frappe.model.add_child(frm.doc, "SIP User", "sip_users");
                        newrow.sip_user_id = String(1000 + i)
                    }
                    frm.refresh()
                },
                '',
                'Generate Users'
            )
        });
	}
});
