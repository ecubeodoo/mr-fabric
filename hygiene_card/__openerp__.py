# -*- coding: utf-8 -*-
{
    'name': "Hygiene Card",

    'summary': "Hygiene Card",

    'description': "Hygiene Card",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report', 'hr'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
