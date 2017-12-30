#-*- coding:utf-8 -*-
########################################################################################
########################################################################################
##                                                                                    ##
##    OpenERP, Open Source Management Solution                                        ##
##    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved       ##
##                                                                                    ##
##    This program is free software: you can redistribute it and/or modify            ##
##    it under the terms of the GNU Affero General Public License as published by     ##
##    the Free Software Foundation, either version 3 of the License, or               ##
##    (at your option) any later version.                                             ##
##                                                                                    ##
##    This program is distributed in the hope that it will be useful,                 ##
##    but WITHOUT ANY WARRANTY; without even the implied warranty of                  ##
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   ##
##    GNU Affero General Public License for more details.                             ##
##                                                                                    ##
##    You should have received a copy of the GNU Affero General Public License        ##
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.           ##
##                                                                                    ##
########################################################################################
########################################################################################

from odoo import models, fields, api
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import Warning

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.clearence_slip.clearence_slip_report'

    @api.model
    def render_html(self,docids, data=None):

        report_obj = self.env['report']
        report = report_obj._get_report_from_name('clearence_slip.clearence_slip_report')
        active_wizard = self.env['clearence.slip'].search([])
        records = self.env['employee.resignation'].browse(docids)
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['clearence.slip'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['clearence.slip'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        accessories_stages = record_wizard.accessories_stages
        resignation = record_wizard.resignation

        employee = self.env['hr.employee'].search([('card_no.id','=',resignation.employee_card.id)])
        fname = ' '
        for x in employee:
            fname = x.fname

        docargs = {
            'doc_ids': docids,
            'doc_model': 'employee.resignation',
            'docs': records,
            'data': data,
            'stage': accessories_stages,
            'resig': resignation,
            'fname': fname
        }

        return report_obj.render('clearence_slip.clearence_slip_report', docargs)