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

class AppointmentLetter(models.AbstractModel):
    _name = 'report.bank_letter.bank_letter_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('bank_letter.bank_letter_report')
        active_wizard = self.env['bank.letter'].search([])

        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['bank.letter'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['bank.letter'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        bank = record_wizard.bank
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to
        branch_code = record_wizard.branch_code
        cheque_no = record_wizard.cheque_no
        authority_letter = record_wizard.authority_letter

        bank_tree = record_wizard.bank_tree

        docargs = {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            'docs': bank,
            'data': data,
            'bank': bank,
            'date_from': date_from,
            'date_to': date_to,
            'branch_code': branch_code,
            'cheque_no': cheque_no,
            'authority_letter': authority_letter,
            'bank_tree': bank_tree,
            }

        return report_obj.render('bank_letter.bank_letter_report', docargs)