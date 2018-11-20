from __future__ import unicode_literals

import frappe
import pprint


def get_context(context):
    # do your magic here
    pprint.pprint(context)
    print('{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}')
    print(frappe.session.user)
    for field in context.web_form_fields:
        if(field.fieldname == 'customer'):
            field.default = 'Raj Moloo'
    print('{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}')
    pprint.pprint(context)
    pass
