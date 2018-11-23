// Copyright (c) 2018, Nayar Joolfoo and contributors
// For license information, please see license.txt

function check_sip_exists(sip_users,sip_user_id){
    for(var i =0 ; i < sip_users.length ; i++) {
        if(sip_users[i].sip_user_id == sip_user_id) {
            return true;
        }
    }
    return false;
}

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
                    var i = 0;
                    while (i < values.no_of_users_to_generate) {
                        var new_sip_user_id = 1000 + i
                        if(check_sip_exists(frm.doc.sip_users,new_sip_user_id) == false){
                            var newrow = frappe.model.add_child(frm.doc, "SIP User", "sip_users");
                            newrow.sip_user_id = String(1000 + i)
                        }
                        else {
                            values.no_of_users_to_generate++
                        }
                        i++
                    }
                    frm.refresh()
                },
                '',
                'Generate Users'
            )
        });
	}
});
