from openerp import models, fields, api
from openerp.exceptions import Warning
from odoo.exceptions import UserError
from openerp.exceptions import UserError


class EcubeMachineInfo(models.Model):
	_name = 'machine.info'
	
	db = fields.Char(string='Data Base')
	odooLogin = fields.Char(string='Login')
	odooPasswd = fields.Char(string='password')
	product_ids=fields.One2many('machine.info.tree','partner_id')

class EcubeMachineInfoError(models.Model):
	_name = 'machine.info.tree'

	ip = fields.Char(string='IP')
	status = fields.Selection([('yes','Active'),('no','InActive')],default='yes')
	partner_id=fields.Many2one('machine.info')