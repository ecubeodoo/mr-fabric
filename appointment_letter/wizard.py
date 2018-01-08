from odoo import models, fields, api

class AppointmentLetterForm(models.Model):
	_name = "appointment.letter"

	employee = fields.Many2one('hr.employee',string="Employee")
	date = fields.Date(string="Confirmation Date")

class AppointmentLettersForm(models.Model):
	_inherit = "appointment.letter"

	@api.multi
	def appoint(self):
		return {
		'type': 'ir.actions.act_window',
		'name': 'Appointment Letter',
		'res_model': 'appointment.letter',
		'view_type': 'form',
		'view_mode': 'form',
		'target' : 'new',
		}