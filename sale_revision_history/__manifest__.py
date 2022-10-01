# -*- encoding: utf-8 -*-
{
	"name": "Sale Revision History",
	"description": """
		Quotation sale revision history
	""",
	"version": "15.0",
	"category": "Sales,Invoicing",
	"author": "Muhammad Bilal",
	"website": "http://www.odoo.com",
	"depends": ["sale","sale_stock","sale_management"],
	"license": 'LGPL-3',
    "support": 'Muhammad Bilal mbilal4m@gmail.com',
	"data": [
		'views/sale_order_views.xml',
		],
	"auto_install": False,
	"installable": True,
	"application": False,
}
