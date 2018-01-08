from openerp import models, fields, api
from openerp.exceptions import Warning
from odoo.exceptions import UserError
from openerp.exceptions import UserError


class EcubeMachineAttendenceError(models.Model):
	_name = 'ecube.attendence.error'
	_rec_name = 'date'
	
	date = fields.Char('Date')

	
	product_ids=fields.One2many('ecube.attendence.error.tree','partner_id')

class EcubeMachineAttendenceErrorTree(models.Model):
	_name = 'ecube.attendence.error.tree'

	machine_ip_error = fields.Char('Machine IP')
	time = fields.Char('Time')
	partner_id=fields.Many2one('ecube.attendence.error')