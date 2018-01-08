# -*- coding: utf-8 -*-

{
    'name': "Salary Sheet",

    'summary': "Salary Sheet",

    'description': "Salary Sheet",

    'author': "Muhammmad Kamran",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report','account','hr','hr_payroll'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}