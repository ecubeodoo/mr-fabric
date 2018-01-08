#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
from datetime import date

class EmployeeGatepass(models.AbstractModel):
    _name = 'report.confirmation_letter.confirmation_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('confirmation_letter.confirmation_report')
        active_wizard = self.env['confirmation.letter'].search([])

        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['confirmation.letter'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['confirmation.letter'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        employee = record_wizard.employee
        date = record_wizard.date

        records = []
        gen = self.env['hr.employee'].search([('id','=',employee.id)])
        if gen:
            records = gen
            records.confirmation_date = date
        else:
            records = self.env['hr.employee'].browse(docids)
            records.name

        docargs = {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            'docs': records,
            'data': data
            }

        return report_obj.render('confirmation_letter.confirmation_report', docargs)