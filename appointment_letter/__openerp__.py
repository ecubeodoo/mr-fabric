# -*- coding: utf-8 -*-
{
    'name': "Appointment Letter",

    'summary': "Appointment Letter",

    'description': "Appointment Letter",

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
