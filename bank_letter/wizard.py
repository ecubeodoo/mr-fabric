from odoo import models, fields, api

class BankLetterForm(models.Model):
	_name = "bank.letter"

	bank = fields.Many2one('account.journal',string="Bank Name")
	date_from = fields.Date(string="Date From")
	date_to = fields.Date(string="Date To")
	branch_code = fields.Char(string="Branch Code")
	cheque_no = fields.Char(string="Cheque No")
	authority_letter = fields.Char(string="Authority Letter No")

	bank_tree = fields.One2many("bank.letter.tree","tree_link")

class BankLetterFormTree(models.Model):
	_name = "bank.letter.tree"

	card_no = fields.Many2one('emp.card.num',string="Card Number")
	employee = fields.Many2one('hr.employee',string="Employee")
	bank = fields.Many2one('account.journal',string="Bank Name")
	account = fields.Char(string="Account No.")

	tree_link = fields.Many2one("bank.letter")

