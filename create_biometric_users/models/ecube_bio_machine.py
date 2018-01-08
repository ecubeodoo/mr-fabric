from openerp import models, fields, api
from openerp.exceptions import Warning
from odoo.exceptions import UserError
from openerp.exceptions import UserError


class EcubeMachine(models.Model):
	_name = 'ecube.machine'
	_description = 'EcubeMachine'
	name = fields.Char('Machine Name')
	machine_ip = fields.Char('Machine IP')
	machine_status = fields.Boolean('Machine Status')