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

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.salary_sheet.salary_sheet'

    @api.model
    def render_html(self,docids, data=None):

        report_obj = self.env['report']
        report = report_obj._get_report_from_name('salary_sheet.salary_sheet')
        active_wizard = self.env['ecube.salary.sheet'].search([])

        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['ecube.salary.sheet'].search([('id','=',emp_list_max)])
        record_wizard_del = self.env['ecube.salary.sheet'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()

        records = record_wizard.tree_link
        to = record_wizard.to
        form = record_wizard.form

        salary_rules = self.env['hr.salary.rule'].search([])

        rules = []
        rule_name = []
        for x in records:
            for y in x.line_ids:
                if y.name not in rule_name:
                    rule_name.append(y.name)
                    rules.append(y)

        allowance = []
        deduction = []
        advances  = []

        for x in salary_rules:
            if x.category_id.name == 'Allowance':
                allowance.append(x)

        for x in salary_rules:
            if x.category_id.name == 'Deduction':
                deduction.append(x)

        for x in salary_rules:
            if x.category_id.name == 'Advances To Employee ':
                advances.append(x)

        departments = []
        for x in records:
            if x.employee_id.department_id not in departments:
                departments.append(x.employee_id.department_id)

        employee = []
        def collect_records(depart):
            del employee[:]
            for x in records:
                if x.employee_id.department_id == depart:
                    employee.append(x)

        def depart_totale(rule):
            amount = 0
            for x in employee:
                for y in x.details_by_salary_rule_category:
                    if y.code == rule:
                        if y.amount:
                            amount = amount + y.amount
            return amount
            
        def get_amount(emp,rule):
            amount = 0
            for x in records:
                if x == emp:
                    for y in x.details_by_salary_rule_category:
                        if y.code == rule:
                            if y.amount:
                                amount = y.amount
            return amount

        def totaled(rule):
            amount = 0
            for x in records:
                for y in x.details_by_salary_rule_category:
                    if y.code == rule:
                        if y.amount:
                            amount = amount + y.amount
            return amount

        def date_getter():
            month = int(form[5:7])
            months_in_words = {
             1:'January',
             2:'February',
             3:'March',
             4:'April',
             5:'May',
             6:'June',
             7:'July',
             8:'August',
             9:'September',
            10:'October',
            11:'November',
            12:'December',
            }

            month = months_in_words[month]
            return month

        docargs   = {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': departments,
            'data': data,
            'allowance': allowance,
            'deduction': deduction,
            'advances': advances,
            'get_amount': get_amount,
            'date_getter': date_getter,
            'totaled': totaled,
            'employee': employee,
            'collect_records': collect_records,
            'depart_totale': depart_totale,
            'rules': rules
        }

        return report_obj.render('salary_sheet.salary_sheet', docargs)