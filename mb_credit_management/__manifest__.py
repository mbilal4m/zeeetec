# -*- coding: utf-8 -*-
{
    'name': "Credit Management",

    'summary': "Credit Management System",

    'description': """
       1: Allow to set credit Limit on partners
       2: Hold Sale order if exceed credit limit
       3: Hold Delivery if exceed credit limit
    """,

    'author': "Muhammad Bilal",
    'website': "https://www.odoo.com",
    'license': 'OPL-1',
    'version': '15.1',
    'category': 'Sale',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 'sale', 'stock'
    ],

    'data': [
        'security/ir.model.access.csv',
        'security/view_res_group.xml',
        'views/view_res_partner.xml',
        'views/view_sale_order.xml',
        'wizard/partner_credit_limit_view_warning.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,
}
