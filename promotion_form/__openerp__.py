# -*- coding: utf-8 -*-
{
    'name': "Promotion Letter",

    'summary': "Promotion Letter",

    'description': "Promotion Letter",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report', 'hr','employee_mr_fabric'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
