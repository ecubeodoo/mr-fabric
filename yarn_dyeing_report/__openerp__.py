# -*- coding: utf-8 -*-
{
    'name': "Yarn Dyeing Vendor Report",

    'summary': "Yarn Dyeing Vendor Report",

    'description': "Yarn Dyeing Vendor Report",

    'author': "yasir rauf",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report','sale'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
