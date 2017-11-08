# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class EmployeeFormExtension(models.Model):
    _inherit = 'hr.employee'

    salaried_person = fields.Boolean(string="Salaried Person")
    rate_per_piece = fields.Boolean(string="Rate Per Piece")
    employee_type = fields.Selection([('temporary','Temporary'),('permanent','Permanent')],string='Employee Type',default='temporary')
    card_no = fields.Char(string='Card No')
    dor = fields.Date(string='DOR')
    religion = fields.Char(string='Religion')
    fname = fields.Char(string='Father Name')
    cnic = fields.Char(string='CNIC NO')
    social_security = fields.Boolean(string="Social Security")
    ss_no = fields.Char(string="SS No")
    eobi = fields.Boolean(string="EOBI")
    eobi_no = fields.Char(string="EOBI No")
