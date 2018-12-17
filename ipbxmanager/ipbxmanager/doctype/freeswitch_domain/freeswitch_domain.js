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
            console.log(frm.doc)
						var myfields = [
                    //{'fieldname': 'no_of_users_to_generate', 'fieldtype': 'Int', 'label': 'No of users to generate', 'reqd': 1}  
                    {'fieldname': 'start_number', 'fieldtype': 'Int', 'label': 'Start Number', 'reqd': 1} ,
                    {'fieldname': 'end_number', 'fieldtype': 'Int', 'label': 'Start Number', 'reqd': 1},
						]
						for(var i = 0; i < frm.doc.sip_groups.length; i++) {
							myfields.push({'fieldname': 'group_' + frm.doc.sip_groups[i].sip_group , 'fieldtype': 'Check', 'label': frm.doc.sip_groups[i].sip_group_name + ':' +  frm.doc.sip_groups[i].sip_group_extension});
						}
            frappe.prompt(myfields,
                function(values){
                    var i = 0;
										console.log(values)
										




                    var new_sip_user_id = values.start_number
                    while (new_sip_user_id <= values.end_number) {
                        //new_sip_user_id = start_number + i
                        if(check_sip_exists(frm.doc.sip_users,new_sip_user_id) == false){
                            var newrow = frappe.model.add_child(frm.doc, "SIP User Child", "sip_users");
                            newrow.sip_user_id = String(new_sip_user_id);
														newrow.sip_groups = '';
														Object.keys(values).forEach(function(key,index){
															if(key.startsWith('group_')) {
																newrow.sip_groups += key + ', \n'
															}
														})
                        }
                        else {
                            //values.no_of_users_to_generate++
                            new_sip_user_id++
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
