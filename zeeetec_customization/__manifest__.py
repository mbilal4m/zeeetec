# -*- encoding: utf-8 -*-
{
	"name": "Zeeetec Customization",
	"summary": "Zeeetec Customization",
	"description": """

	""",
	"version": "15.0",
	"category": "Sales",
	"author": "Muhammad Bilal",
	"website": "http://www.odoo.com",
	"depends": ["sale", "crm", "industry_fsm_sale", "account"],
	"license": 'LGPL-3',
    'support': 'Muhammad Bilal mbilal4m@gmail.com',
	"data": [
		# 'security/ir.model.access.csv',
		'views/sale_order_view.xml',
		'views/account_move_view.xml',
		],
	"auto_install": False,
	"installable": True,
	"application": False,
}
