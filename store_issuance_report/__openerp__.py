# -*- coding: utf-8 -*-
{
    'name': "Store Issuance Report",

    'summary': "Store Issuance Report",

    'description': "Store Issuance Report",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report','purchase'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
