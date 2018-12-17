import pprint
import frappe

def get_context(context):
    pprint.pprint(frappe)
    pprint.pprint(context)
    context['custom_content'] = 'Hub featured page custom content'
