# -*- coding: utf-8 -*-
{
    'name': 'Travel management',
    'version': '1.0',
    'summary': 'travel management software',
    'sequence': -100,
    'description': "travel management",
    'category': 'productivity',
    'website': 'https://www.odoo.com/page/billing',
    'depends': ['sale','mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/securitytravel.xml',
        'data/sequence.xml',
        'data/data.xml',
        'data/service_cron.xml',
         'views/customer.xml',
         'views/sale.xml',
         'views/tourpackage.xml',
        'views/configuration.xml'

    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
