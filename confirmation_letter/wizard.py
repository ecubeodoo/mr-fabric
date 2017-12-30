# #-*- coding:utf-8 -*-
# ##############################################################################
# #
# #    OpenERP, Open Source Management Solution
# #    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
# #
# #    This program is free software: you can redistribute it and/or modify
# #    it under the terms of the GNU Affero General Public License as published by
# #    the Free Software Foundation, either version 3 of the License, or
# #    (at your option) any later version.
# #
# #    This program is distributed in the hope that it will be useful,
# #    but WITHOUT ANY WARRANTY; without even the implied warranty of
# #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #    GNU Affero General Public License for more details.
# #
# #    You should have received a copy of the GNU Affero General Public License
# #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #
# ##############################################################################
from odoo import models, fields, api

class GenerateConfirmationLetter(models.Model):
	_name = "confirmation.letter"

	card_no = fields.Many2one('emp.card.num',string="Card No.", required="1")
	employee = fields.Many2one('hr.employee',string="Employee")
	date = fields.Date(string="Confirmation Date")

	@api.onchange('card_no')
	def onchange_employee_card(self):
		employee = self.env['hr.employee'].search([('card_no.id','=',self.card_no.id)])
		self.employee = employee.id

class GenerateConfirmationLetter(models.Model):
	_inherit = "hr.employee"    

	@api.model
	def create_report(self):
		return {
		'type': 'ir.actions.act_window',
		'name': 'Product Profile',
		'res_model': 'hr.employee',
		'view_type': 'form',
		'view_mode': 'form',
		'target' : 'new',
		}