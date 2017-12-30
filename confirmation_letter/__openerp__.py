# -*- coding: utf-8 -*-
{
    'name': "Confirmation Letter",

    'summary': "Confirmation Letter",

    'description': "Confirmation Letter",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.pk",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report', 'hr','employee_mr_fabric'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
