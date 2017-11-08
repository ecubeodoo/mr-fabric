# -*- coding: utf-8 -*-
{
    'name': "Employee Card mr.fabrics",

    'summary': "Employee Card mr.fabrics",

    'description': "Employee Card mr.fabrics",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report', 'purchase'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
