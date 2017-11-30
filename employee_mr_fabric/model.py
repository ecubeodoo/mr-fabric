# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from datetime import date, datetime, timedelta

class EmployeeFormExtension(models.Model):
    _inherit = 'hr.employee'

    salaried_person = fields.Boolean(string="Salaried Person")
    rate_per_piece = fields.Boolean(string="Rate Per Piece")
    employee_type = fields.Selection([('temporary','Temporary'),('permanent','Permanent')],string='Employee Type',default='temporary')
    card_no = fields.Char(string='Card No')
    dor = fields.Date(string='DOR')
    doj = fields.Date(string='Date of Joining')
    doi = fields.Date(string='Date of issue',default=fields.Date.today)
    religion = fields.Char(string='Religion')
    fname = fields.Char(string='Father Name')
    cnic = fields.Char(string='CNIC NO')
    social_security = fields.Boolean(string="Social Security")
    ss_no = fields.Char(string="SS No")
    eobi = fields.Boolean(string="EOBI")
    eobi_no = fields.Char(string="EOBI No")
    name_card = fields.Char(string="Name")

    @api.onchange('name','card_no')
    def onchange_namecard(self):
        addition = str(self.name) + ' - ' + str(self.card_no)
        self.name_card = addition

class HrOvertime(models.Model):
    _name = 'hr.overtime'
    _rec_name = 'rec_name'

    date = fields.Date(string="Date", required= True)
    department = fields.Many2one('hr.department',string="Department")
    total_overtime_hours = fields.Float(string="Total Overtime Hours") 
    total_overtime_amount = fields.Float(string="Total Overtime Amount")
    tree_link = fields.One2many('hr.overtime.tree','tree_linked')
    rec_name = fields.Char(String="Rec name")

    @api.onchange('date','department')
    def onchange_depart(self):
        self.rec_name = str(self.department.name) + ',' + str(self.date)

    @api.onchange('tree_link')
    def onchange_tree(self):
        actual_overtime = 0
        total_overtime = 0
        for x in self.tree_link:
            actual_overtime = actual_overtime + x.actual_overtime_hours
            total_overtime = total_overtime + x.overtime_amount

        self.total_overtime_hours = actual_overtime
        self.total_overtime_amount = total_overtime*actual_overtime

class HrOvertimeTreeView(models.Model):
    _name = 'hr.overtime.tree'

    employee = fields.Many2one('hr.employee',string="Employee", required= True)
    planed_overtime_hours = fields.Float(string="Planed Overtime Hours") 
    actual_overtime_hours = fields.Float(string="Actual Overtime Hours")
    overtime_amount = fields.Float(string="Overtime Amount")
    remarks = fields.Char(string="Remarks")

    tree_linked = fields.Many2one('hr.overtime')

    @api.onchange('actual_overtime_hours')
    def onchange_actual(self):

        contract = self.env['hr.contract'].search([('employee_id.id','=',self.employee.id)])

        self.overtime_amount = ((contract.wage/26)/8)*self.actual_overtime_hour