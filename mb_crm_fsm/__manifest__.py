# -*- encoding: utf-8 -*-
{
	"name": "CRM Field Services",
	"summary": "Create Field Service from CRM",
	"description": """

	""",
	"version": "15.0",
	"category": "Sales",
	"author": "Muhammad Bilal",
	"website": "http://www.odoo.com",
	"depends": ["sale","crm","industry_fsm_sale"],
	"license": 'LGPL-3',
    'support': 'Muhammad Bilal mbilal4m@gmail.com',
	"data": [
		'security/security.xml',
		'security/ir.model.access.csv',
		'wizard/crm_fsm_wizard_view.xml',
		'views/crm_views.xml',
		'views/project_task.xml',
		],
	"auto_install": False,
	"installable": True,
	"application": False,
}
