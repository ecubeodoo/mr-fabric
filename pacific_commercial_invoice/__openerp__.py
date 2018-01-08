# -*- coding: utf-8 -*-
{
    'name': "Pacific Commercial Invoice",

    'summary': "Pacific Commercial Invoice",

    'description': "Pacific Commercial Invoice",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.pk",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report', 'account'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
