# -*- coding: utf-8 -*-
{
    'name': "Create BioMetric Useres",

    'summary': "",

    'description': "Fields are added",

    'author': "Ehtisham Faisal",
    'website': "http://www.oxenlab.com",


    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_attendance'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/ecube_bio_menu_items.xml',
        'views/ecube_bio_hr_employee.xml',
        'views/ecube_bio_raw_attendance.xml',
        'views/ecube_bio_machine.xml',
        'views/ecube_bio_attendence_error.xml',
        'views/ecube_machine_info.xml',
    ],
}
