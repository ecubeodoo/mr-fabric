# -*- coding: utf-8 -*-
{
    'name': "Employee Gatepass",

    'summary': "Employee Gatepass",

    'description': "Employee Gatepass",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.pk",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report', 'hr'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
