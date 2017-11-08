# -*- coding: utf-8 -*-
{
    'name': "Yarn Requirement Report",

    'summary': "Yarn Requirement Report",

    'description': "Yarn Requirement Report",

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
