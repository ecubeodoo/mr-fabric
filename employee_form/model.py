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

class EmployeeFormGenrator(models.AbstractModel):
    _name = 'report.employee_form.employee_form_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('employee_form.employee_form_report')
        active_wizard = self.env['employee.form'].search([])

        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['employee.form'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['employee.form'].search([('id','!=',emp_list_max)])
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

        def salary(attr):
            contract = self.env['hr.contract'].search([('employee_id.id','=',attr.id)])

            return contract.wage

        docargs = {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            'docs': records,
            'data': data,
            'salary': salary
            }

        return report_obj.render('employee_form.employee_form_report', docargs)