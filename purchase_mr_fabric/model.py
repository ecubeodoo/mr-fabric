# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from openerp.exceptions import Warning, ValidationError, UserError

class accessories(models.Model):
	_name = 'purchase.accessories'
	_rec_name = 'sr_no'
	_inherit = ['mail.thread', 'ir.needaction_mixin']
# fhgfhfdghdf
	sr_no = fields.Char(string="Sr no")
	wonumber = fields.Many2one('mrp.production',string="WO No",)
	style = fields.Char(string="Style No")
	date = fields.Date(string="Date")
	merchant = fields.Many2one('hr.employee',string="Merchant")

	vendor = fields.Many2one('res.partner',string="Vendor Name", required= True)
	warehouse = fields.Many2one('stock.picking.type',string="Warehouse")
	destination_location = fields.Many2one('stock.location',string="Destination Location Zone")
	source_location = fields.Many2one('stock.location',string="Source Location Zone")
	delivery = fields.Many2one('stock.picking',string="Delivery")

	customer = fields.Many2one('res.partner',string="Customer")
	delivery_date = fields.Date(string="Delivery Date")

	seq_code = fields.Char(string="Security Code")
	req_code = fields.Char(string="Req Code")
	
	accessories_stages = fields.Selection([
		('draft', 'Draft'),
		('recieved', 'Received'),
		('customer_approval', 'Customer Approval'),
		('rejected', 'Rejected'),
		('approved', 'Approved'),
		('validate', 'Validate'),
		('cancel', 'Cancel'),
		],default='draft')

	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")
	access_po_num = fields.Many2one('purchase.order',string="Po Num")

	tree_link = fields.One2many('purchase.accessories.tree','tree')

	@api.model
	def create(self, vals):
		vals['sr_no'] = self.env['ir.sequence'].next_by_code('purchase.accessories')
		new_record = super(accessories, self).create(vals)

		return new_record
						
	@api.multi
	def in_draft(self):
		self.accessories_stages = "draft"
						
	@api.multi
	def in_recieved(self):
		self.accessories_stages = "recieved"

		connect_po = self.env['purchase.order'].search([('id','=',self.access_po_num.id)])

		for x in self.tree_link:
			for y in connect_po.order_line:
				if y.product_id.id == x.product.id:
					y.qty_received = y.qty_received + x.recieved

		for x in self.tree_link:
			if x.qty > x.recieved:
				amount = x.qty - x.recieved

				purchase_accessories_env=self.env['purchase.accessories']
				purchase_accessories_record=purchase_accessories_env.create({
					'vendor' : self.vendor.id,
					'wonumber' : self.wonumber.id,
					'access_po_num' : self.access_po_num.id
				})

				for x in self.tree_link:
					lines=self.env['purchase.accessories.tree'].create({
					'product' : x.product.id,
					'unit_measurement' : x.unit_measurement.id,
					'qty' : amount,
					'to_recieve' : amount,
					'price' : x.price,
					'tree' : purchase_accessories_record.id,
				})


	@api.multi
	def in_customer_approval(self):
		self.accessories_stages = "customer_approval"

	@api.multi
	def in_rejected(self):
		self.accessories_stages = "rejected"

	@api.multi
	def in_approved(self):
		self.accessories_stages = "approved"

	@api.multi
	def in_validate(self):
		self.accessories_stages = "validate"

		create_reorder = self.env['stock.picking'].create({
			'partner_id': self.vendor.id,
			'min_date': self.date,
			'origin': self.sr_no,
			'picking_type_id': self.warehouse.id,
			'location_id': self.source_location.id,
			'location_dest_id': self.destination_location.id,

		})

		for x in self.tree_link:
			create_variants = self.env['stock.move'].create({
				'product_id': x.product.id,
				'product_uom_qty': x.recieved,
				'product_uom': x.unit_measurement.id,
				'picking_id': create_reorder.id,
				'location_id': create_reorder.location_id.id,
				'name': x.product.name,
				'location_dest_id': create_reorder.location_dest_id.id,
			})

		self.delivery = create_reorder.id

	@api.multi
	def in_cancel(self):
		self.accessories_stages = "cancel"

class yarn(models.Model):
	_name = 'purchase.yarn'
	_rec_name = 'sr_no'
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	sr_no = fields.Char(string="Sr no")
	wonumber = fields.Char(string="WO No", required=True)
	style = fields.Char(string="Style No")
	date = fields.Date(string="Date")
	merchant = fields.Char(string="Merchant Name")
	amt_total = fields.Float(string="Amount Inc Tax",compute='total_tax',store=True)
	total = fields.Float(string="Amount",compute='total_tree',store=True)
	vendor = fields.Many2one('res.partner',string="Vendor Name", required= True)
	broker = fields.Many2one('res.partner',string="Broker")
	warehouse = fields.Many2one('stock.picking.type',string="Warehouse")
	destination_location = fields.Many2one('stock.location',string="Destination Location Zone")
	source_location = fields.Many2one('stock.location',string="Source Location Zone")
	delivery = fields.Many2one('stock.picking',string="Delivery")
	tax_id = fields.Many2one('account.tax',string="Tax")
	wo_num = fields.Many2one('mrp.production',string="WO#")

	tree_link = fields.One2many('purchase.accessories.tree','yarn_tree')

	@api.model
	def create(self, vals):
		vals['sr_no'] = self.env['ir.sequence'].next_by_code('purchase.yarn')
		new_record = super(yarn, self).create(vals)

		return new_record

	@api.depends('tree_link')
	def total_tree(self):
		self.total = 0.0
		for x in self.tree_link:
			self.total = x.sub_total + self.total

		self.total

	@api.depends('tax_id')
	def total_tax(self):
		if self.tax_id:
			value = self.total * self.tax_id.amount / 100
			self.amt_total = self.total + value

class yarnApproval(models.Model):
	_name = 'yarn.approval'
	_rec_name = 'date'
	_inherit = ['mail.thread', 'ir.needaction_mixin']

	date = fields.Date(string="Date")
	start_date = fields.Date(string="Start Date")
	end_date = fields.Date(string="End Date")

	won = fields.Many2one('mrp.production', string="Word order No.")
	yarn_count = fields.Many2one('product.product', string="Yarn Count")

	week = fields.Char(string="Week")

	tree_link = fields.One2many('yarn.requirement.tree','yarn_approval_tree')

	@api.multi
	def get_values(self):
		require_lines = self.env['yarn.requirement.tree'].search([])
		dates = []
		w_orders = []
		weeks = []
		changes = 0

		if self.start_date and self.end_date:
			dates = require_lines.search([('delv_date','>=',self.start_date),('delv_date','<=',self.end_date)])
			++changes
		else:
			dates = require_lines

		if self.won:
			w_orders = dates.search([('won.id','=',self.won.id)])
			++changes
		else:
			w_orders = dates

		if self.week:
			weeks = w_orders.search([('week','=',self.week)])
			++changes
		else:
			weeks = w_orders

		if weeks == require_lines and changes == 0:
			return
		else:
			self.tree_link = weeks

class accessories_tree(models.Model):
	_name = "purchase.accessories.tree"

	product = fields.Many2one('product.product',string="Product", required=True)
	unit_measurement = fields.Many2one('product.uom', string="Unit of Measurement")

	to_recieve = fields.Float(string="To Recieve")
	recieved = fields.Float(string="Recieved")
	rejected = fields.Float(string="Rejected")
	price = fields.Float(string="Unit Price")
	qty = fields.Float(string="Qty")
	sub_total = fields.Float(string="Amount")
	tree = fields.Many2one('purchase.accessories')
	yarn_tree = fields.Many2one('purchase.yarn')
	
	remarks = fields.Char(string="Remarks")

	@api.onchange('price','qty')
	def sub_total_tree(self):
		self.sub_total = self.qty * self.price

	@api.onchange('product')
	def unit_tree(self):
		product = self.env['product.product'].search([('id','=',self.product.id)])
		self.unit_measurement = product.uom_id

class YarnRequirement(models.Model):
	_name = "yarn.requirement"
	_rec_name = 'date'

	date = fields.Date("Date" ,required = True)
	won = fields.Many2many('mrp.production',string="Work Order No")
	stage = fields.Selection([('draft', 'Draft'),('val', 'Validate'),('wait', 'Waiting for Approval'),('approve', 'Approved')],default = 'draft') 
	tree_link = fields.One2many('yarn.requirement.tree','yarn_tree')
	@api.multi
	def in_draft(self):
		self.stage = "draft"

	@api.multi
	def val(self):
		self.stage = "val"

	@api.multi
	def wait(self):
		self.stage = "wait"

	@api.multi
	def approve(self):
		self.stage = "approve"

	@api.multi
	def cancel(self):
		self.stage = "draft"

class YarnRequirementTree(models.Model):
	_name = "yarn.requirement.tree"

	product = fields.Many2one('product.product',string="Yarn Count", required=True)
	won = fields.Many2many('mrp.production',string="W/O")
	buyer = fields.Many2many('res.partner',string="Buyer")
	prod_type = fields.Many2one('purchase.product.type',string="Product Type")
	delv_date = fields.Date("Delivery Date")
	qty = fields.Float("Quantity (KG)")
	nob = fields.Float("No of Bags")
	rate = fields.Many2many('yarn.rates',string="Rate")
	yarn = fields.Many2one('purchase.brand',string="Yarn Brand")
	appr_rate = fields.Many2one('yarn.rates',string="Approved Rate")
	unit_price = fields.Float("Unit Price")
	week = fields.Float("Week")
	broker = fields.Many2one('res.partner',"Broker")

	yarn_tree = fields.Many2one('yarn.requirement')

	yarn_approval_tree = fields.Many2one('yarn.approval')

	@api.onchange('appr_rate')
	def appr_rate_change(self):
		self.unit_price = self.appr_rate.name

	@api.onchange('qty')
	def qty_change(self):
		if self.product.net_weight > 0 and self.qty:
			self.nob= self.qty / self.product.net_weight

	@api.onchange('won')
	def won_change(self):
		buyers = []
		for x in self.won:
			work_order = self.env['mrp.production'].search([('id','=',x.id)])
			for x in work_order:
				if work_order.buyer:
					buyers.append(work_order.buyer.id)

		self.buyer = buyers

class YarnRate(models.Model):
	_name = "yarn.rates"

	name = fields.Char("Rate" ,required=True)
	partner = fields.Many2one('res.partner',"Partner")

class PurchaseOrderExt(models.Model):
	_inherit = 'purchase.order'

	wo_no = fields.Many2one('mrp.production',string='WO No',required = True)
	style = fields.Char("Style No")
	merchant = fields.Many2one('hr.employee',string="Merchant Name")
	order_line2 = fields.One2many('purchase.order.line','order_id')
	purchase_recharge_count = fields.Integer(string="Recharge",compute='act_show_accessories_deliveries')
	ttype = fields.Selection([
		('yarn', 'Yarn'),
		('fabric', 'Fabric'),
		('accessories', 'Accessories'),
		('general', 'General')
		],default='yarn', required=True, string="Type")

	@api.multi
	def custom_button(self):

		prev_order = self.env['purchase.accessories'].search([('access_po_num','=',self.id)])

		if prev_order:
			raise ValidationError("Accessories Order against this PO already Exist")

		else:
			purchase_accessories_env=self.env['purchase.accessories']
			purchase_accessories_record=purchase_accessories_env.create({
				'vendor' : self.partner_id.id,
				'wonumber' : self.wo_no.id,
				'access_po_num' : self.id
				})
			for x in self.order_line:
				lines=self.env['purchase.accessories.tree'].create({
				'product' : x.product_id.id,
				'unit_measurement' : x.product_uom.id,
				'qty' : x.product_qty,
				'to_recieve' : x.product_qty,
				'price' : x.price_unit,
				'tree' : purchase_accessories_record.id,
				})

	@api.one 
	def act_show_accessories_deliveries(self):
		self.purchase_recharge_count = self.env['purchase.accessories'].search_count([('access_po_num','=',self.id)])

class PurchaseOrderLineExt(models.Model):
	_inherit = 'purchase.order.line'

	nob = fields.Float("No of Bags")

	@api.onchange('product_qty')
	def qty_change(self):
		if self.product_id.net_weight > 0 and self.product_qty:
			self.nob= self.product_qty / self.product_id.net_weight

class StockPickingExt(models.Model):
	_inherit = 'stock.picking'

	req_code = fields.Char("Requisition Code")
	sec_code = fields.Char("Security Code")

class YarnDyeing(models.Model):
	_name = "yarn.dyeing"

	name = fields.Many2one('res.partner',string="To",required = True)
	date = fields.Date(" Start Date")
	c_date = fields.Date("Completion Date")
	buyer = fields.Many2many('res.partner',string="Buyer")
	style = fields.Char("Style No")
	won = fields.Many2many('mrp.production',string="Work Order No")
	delv_date = fields.Date("Delivery Date")
	primary = fields.Many2one('purchase.primary', string="Primary")
	secondary = fields.Many2one('purchase.secondary', string = "Secondary")
	des = fields.Text("Note")
	mf = fields.Char("MF No")
	req_code = fields.Char("Requisition Code")
	sec_code = fields.Char("Security Code")
	tree_link = fields.One2many('yarn.dyeing.tree','yarn_tree')
	recharge_count = fields.Integer(string="Recharge", compute="_load_list")

	source_location = fields.Many2one('stock.location',string="Source Location")
	destination_location = fields.Many2one('stock.location',string="Destination Location")
	warehouse_id = fields.Many2one('stock.location',string="Warehouse")
	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")
	
	@api.one
	def _load_list(self):
		self.recharge_count = self.env['yarn.wizard.class'].search_count([('tree_id','=',self.id)])

	stage = fields.Selection([('draft', 'Draft'),
		('sent', 'Sent'),
		('in_house', 'In House'),
		('complete', 'Complete')
		],default = 'draft') 

	@api.onchange('won')
	def get_buyer(self):
		buyers = []
		styles = ' '
		for x in self.won:
			work_order = self.env['mrp.production'].search([('id','=',x.id)])
			if work_order.delivery:
				self.delv_date = work_order.delivery
			if work_order.buyer:
				buyers.append(work_order.buyer.id)
			if work_order.style_no:
				if styles == ' ':
					styles = work_order.style_no
				else:
					styles = styles + ', ' + work_order.style_no

		self.buyer = buyers
		self.style = styles

	@api.multi
	def in_draft(self):
		self.stage = "draft"

	@api.multi
	def in_sent(self):
		self.stage = "sent"

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.source_location.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.destination_location.id,
			'origin': 'Yarn Dyeing',
		})

		for x in self.tree_link:
			create_inventory_lines = inventory_lines.create({
				'product_id':x.yarn.id,
				'product_uom_qty':x.issue_qty,
				'product_uom': 1,
				'location_id':15,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': 9,
				})

	@api.multi
	def in_house(self):
		self.stage = "in_house"

	@api.multi
	def complete(self):
		self.stage = "complete"

	@api.multi
	def yarn_receiving(self):
		return {
		'type': 'ir.actions.act_window',
		'name': 'Yarn Receiving',
		'res_model': 'yarn.wizard.class',
		'view_type': 'form',
		'view_mode': 'form',
		}

class YarnDyeingTree(models.Model):
	_name = "yarn.dyeing.tree"

	won = fields.Many2one('mrp.production',string="W/O",required = True)
	color = fields.Many2one('purchase.color',string="Colors")
	yarn = fields.Many2one('product.product',string="Yarn Count")
	lot = fields.Many2one('purchase.lot',string="Lot No")
	rate = fields.Float("Rate")
	issue_qty = fields.Float("Issue Qty")
	receive_qty = fields.Float("Received Qty (Kg)")
	receiveable_qty = fields.Float("Receivable Qty (Kg)")
	blc = fields.Char("Balance" ,compute='_blc')
	wastage = fields.Char("Actual Wastage" ,compute='_wastage')
	agree_wastage = fields.Float("Agreed Wastage")
	std = fields.Binary("STD")
	yarn_tree = fields.Many2one('yarn.dyeing')
	
	@api.one
	@api.depends('receiveable_qty','receive_qty')
	def _blc(self):
		balance = self.receive_qty - self.receiveable_qty
		if balance < 0:
			self.blc = balance
		if balance > 0:
			self.blc = "+" + str(balance)

	@api.one
	@api.depends('issue_qty','blc')
	def _wastage(self):
		if self.issue_qty:
			if self.blc:
				waste = ((float(self.blc) / self.issue_qty)* 100)
				if waste < 0:
					self.wastage = str("{0:.2f}".format(waste * (-1))) + "%"
				if waste > 0:
					self.wastage = str("{0:.2f}".format(waste)) + "%"   

	@api.onchange('issue_qty','agree_wastage')
	def get_reciving(self):
		if self.issue_qty > 0.0:
			self.receiveable_qty = self.issue_qty - ((self.agree_wastage * self.issue_qty)/ 100)  

	@api.onchange('receive_qty')
	def get_recived(self):
		recived = self.receive_qty
		reciveable = self.receiveable_qty + (self.receiveable_qty*0.1)
		print reciveable
		print "----------------"

		if recived > reciveable:
			self.receive_qty = self.receiveable_qty
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Recived Quantity should not be greater than the Reciveable Quantity'}}

class FabricDyeing(models.Model):
	_name = "fabric.dyeing"

	name = fields.Many2one('res.partner',string="To", required=True)
	date = fields.Date("Start Date")
	c_date = fields.Date("Completion Date")
	subject = fields.Char("Subject")
	buyer = fields.Many2many('res.partner',string="Buyer")
	style = fields.Char("Style No")
	won = fields.Many2many('mrp.production',string="Work Order No")
	delv_date = fields.Date("Delivery Date")
	primary = fields.Many2one('purchase.primary', string="Primary")
	secondary = fields.Many2one('purchase.secondary', string = "Secondary")
	des = fields.Text("Note")
	req_code = fields.Char("Requisition Code")
	sec_code = fields.Char("Security Code")
	tree_link = fields.One2many('fabric.dyeing.tree','yarn_tree')
	recharge_count = fields.Integer(string="Recharge", compute="_load_list")

	stage = fields.Selection([('draft', 'Draft'),
		('sent', 'Sent'),
		('in_house', 'In House'),
		('complete', 'Complete')
		],default = 'draft') 

	source_location = fields.Many2one('stock.location',string="Source Location")
	destination_location = fields.Many2one('stock.location',string="Destination Location")
	warehouse_id = fields.Many2one('stock.location',string="Warehouse")
	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")

	@api.onchange('won')
	def get_buyer(self):
		buyers = []
		styles = ' '
		for x in self.won:
			work_order = self.env['mrp.production'].search([('id','=',x.id)])
			if work_order.delivery:
				self.delv_date = work_order.delivery
			if work_order.buyer:
				buyers.append(work_order.buyer.id)
			if work_order.style_no:
				if styles == ' ':
					styles = work_order.style_no
				else:
					styles = styles + ', ' + work_order.style_no

		self.buyer = buyers
		self.style = styles

	@api.one
	def _load_list(self):
		self.recharge_count = self.env['fabric.wizard.class'].search_count([('tree_id','=',self.id)])

	@api.multi
	def in_draft(self):
		self.stage = "draft"

	@api.multi
	def in_sent(self):
		self.stage = "sent"

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.source_location.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.destination_location.id,
			'origin': 'Fabric Dyeing',
		})

		for x in self.tree_link:
			create_inventory_lines = inventory_lines.create({
				'product_id':x.fabric.id,
				'product_uom_qty':x.issue_qty,
				'product_uom': x.fabric.uom_id.id,
				'location_id':15,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': 9,
				})

	@api.multi
	def in_house(self):
		self.stage = "in_house"

	@api.multi
	def in_complete(self):
		self.stage = "complete"

	@api.multi
	def fabric_receiving(self):

		return {
		'type': 'ir.actions.act_window',
		'name': 'Fabric Receiving',
		'res_model': 'fabric.wizard.class',
		'view_type': 'form',
		'view_mode': 'form',
		'context': {'fabric_no':self.id},
		}

class FabricDyeingTree(models.Model):
	_name = "fabric.dyeing.tree"

	won = fields.Many2one('mrp.production',string="W/O",required = True)
	color = fields.Many2one('purchase.color',string="Colors")
	lot = fields.Many2one('purchase.lot',string="Lot No")
	fabric = fields.Many2one('product.product',"Fabric")
	dia = fields.Many2one('purchase.dia' , string="Dia")
	gauge = fields.Many2one('purchase.gauge' , string="Gauge")
	ndl = fields.Many2one('purchase.ndl' , string="NDL")
	width = fields.Many2one('purchase.width' , string="Width")
	gsm = fields.Many2one('purchase.gsm' , string="GSM")
	process = fields.Many2one('purchase.process' , string="Process")
	rate = fields.Float("Rate")
	issue_qty = fields.Float("Issue Qty")
	receive_qty = fields.Float("Received Qty (Kg)")
	receivable_qty = fields.Float("Receivable Qty (Kg)")
	blc = fields.Float("Balance" ,compute='_blc')
	wastage = fields.Char("Actual Wastage" ,compute='_wastage', digits=(16,2))
	agree_wastage = fields.Float(string="Agreed Wastage")
	yarn_tree = fields.Many2one('fabric.dyeing')

	@api.one
	@api.depends('receivable_qty','receive_qty')
	def _blc(self):
		balance = self.receive_qty - self.receivable_qty
		if balance < 0:
			self.blc = balance
		if balance > 0:
			self.blc = "+" + str(balance)

	@api.one
	@api.depends('issue_qty','blc')
	def _wastage(self):
		if self.issue_qty:
			if self.blc:
				waste = ((self.blc / self.issue_qty)* 100)
				if waste < 0:
					self.wastage = str("{0:.2f}".format(waste * (-1))) + "%"
				if waste > 0:
					self.wastage = str("{0:.2f}".format(waste)) + "%"

	@api.onchange('issue_qty','agree_wastage')
	def get_reciving(self):
		if self.issue_qty > 0.0:
			self.receivable_qty = self.issue_qty - ((self.agree_wastage * self.issue_qty)/ 100)

	@api.onchange('receive_qty')
	def get_recived(self):
		recived = self.receive_qty
		reciveable = self.receivable_qty + (self.receivable_qty*0.1)
		print reciveable
		print "----------------"

		if recived > reciveable:
			self.receive_qty = self.receivable_qty
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Recived Quantity should not be greater than the Reciveable Quantity'}}

class ResPartnerExt(models.Model):
	_inherit = "res.partner"
	_rec_name = 'ttype'

	knitting = fields.Boolean("Knitting")
	buyer = fields.Boolean("Buyer")
	broker = fields.Boolean("Broker")
	mill = fields.Boolean("Mill")
	ttype = fields.Selection([('dye', 'Dyeing'),
		('knit', 'Knitting')
		],string = "Type") 

class FabricKnitting(models.Model):
	_name = "fabric.knitting"

	name = fields.Many2one('res.partner',string="To", required=True)
	date = fields.Date("Order Date" , required=True)
	buyer = fields.Many2many('mrp.production',string="Buyer")
	won = fields.Many2many('mrp.production',string="W/O")
	delv_date = fields.Date("Delivery Date")
	c_date = fields.Date("Order Completion Date")
	style = fields.Char("Style No.")
	req_code = fields.Char("Requisition Code")
	sec_code = fields.Char("Security Code")
	tree_link = fields.One2many('fabric.knitting.tree','fabric_tree')
	recharge_count = fields.Integer(string="Recharge", compute="_load_list")
	
	stage = fields.Selection([('draft', 'Draft'),
		('sent', 'Sent'),
		('in_house', 'In House'),
		('complete', 'Complete'),
		('cancel', 'Cancel')
		],default = 'draft') 

	source_location = fields.Many2one('stock.location',string="Source Location")
	destination_location = fields.Many2one('stock.location',string="Destination Location")
	warehouse_id = fields.Many2one('stock.location',string="Warehouse")
	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")

	# @api.onchange('won')
	# def get_buyer(self):
	# 	buyers = []
	# 	styles = ' '
	# 	for x in self.won:
	# 		work_order = self.env['mrp.production'].search([('id','=',x.id)])
	# 		if work_order.delivery:
	# 			self.delv_date = work_order.delivery
	# 		if work_order.buyer:
	# 			buyers.append(work_order.buyer.id)
	# 		if work_order.style_no:
	# 			if styles == ' ':
	# 				styles = work_order.style_no
	# 			else:
	# 				styles = styles + ', ' + work_order.style_no

	# 	self.buyer = buyers
	# 	self.style = styles

	@api.one
	def _load_list(self):
		self.recharge_count = self.env['knit.wizard.class'].search_count([('tree_id','=',self.id)])

	@api.multi
	def knit_receiving(self):
		return {
		'type': 'ir.actions.act_window',
		'name': 'Knitting Receiving',
		'res_model': 'knit.wizard.class',
		'view_type': 'form',
		'view_mode': 'form',
		}

	@api.multi
	def in_draft(self):
		self.stage = "draft"

	@api.multi
	def in_sent(self):
		self.stage = "sent"

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.source_location.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.destination_location.id,
			'origin': 'Fabric Knitting Dyeing',
		})

		for x in self.tree_link:
			create_inventory_lines = inventory_lines.create({
				'product_id':x.fabric.id,
				'product_uom_qty':x.received,
				'product_uom': x.fabric.uom_id.id,
				'location_id':15,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': 9,
				})

	@api.multi
	def in_house(self):
		self.stage = "in_house"

	@api.multi
	def in_complete(self):
		self.stage = "complete"

	@api.multi
	def in_cancel(self):
		self.stage = "cancel"

class FabricKnittingTree(models.Model):
	_name = "fabric.knitting.tree"

	won = fields.Many2many('mrp.production',string="W/O", required=True)
	fabric = fields.Many2one('product.product',string="Fabric")
	yarn = fields.Many2many('product.template',string="Yarn")
	lot = fields.Many2one('purchase.lot',string="Lot No")
	sl = fields.Many2one('purchase.sl' , string="S.L")
	otm = fields.Many2one('purchase.otm' , string="OTM")
	dia = fields.Many2one('purchase.dia' , string="Dia")
	gauge = fields.Many2one('purchase.gauge' , string="Gauge")
	ndl = fields.Many2one('purchase.ndl' , string="NDL")
	required = fields.Float("Required (KG)")
	received = fields.Float("Received (KG)")
	balance = fields.Float("Balance" ,compute='_balance')
	wastage = fields.Char("Wastage Percentage" ,compute='_wastage')   
	rate  = fields.Float("Rates") 
	a_wastage  = fields.Char("Agreed Wastage") 
	fabric_tree = fields.Many2one('fabric.knitting')

	@api.one
	@api.depends('required','received')
	def _balance(self):
		if self.received and self.required:
			self.balance = self.received - self.required

	@api.one
	@api.depends('required','received','balance')
	def _wastage(self):
		if self.balance < 0:
			if self.received > 0.0 and self.required > 0.0:
				self.wastage = str("{0:.2f}".format((-1*((self.balance) / self.required)* 100 ))) + "%"

	@api.onchange('fabric')
	def get_yarn(self):
		if self.fabric:
			self.yarn = self.fabric.yarn

class ProductExt(models.Model):
	_inherit = 'product.template'

	ttype = fields.Selection([
		('yarn', 'Yarn'),
		('fabric', 'Fabric'),
		('accessories', 'Accessories'),
		('general', 'General Products'),
		('thread', 'Thread')
		],default='yarn', required=True, string="Type")

class ProductVariantsExt(models.Model):
	_inherit = 'product.product'

	ttype = fields.Selection([
		('yarn', 'Yarn'),
		('fabric', 'Fabric'),
		('accessories', 'Accessories'),
		('general', 'General Products'),
		('thread', 'Thread')
		],default='yarn', required=True, string="Type")

	accessories_type = fields.Selection([
		('wo', 'WO'),
		('thread', 'Thread'),
		('bag', 'Poly Bag'),
		('part', 'Parts')
		],default='wo', string="Accessories Type")

	net_weight = fields.Float("Net Weight")
	yarn = fields.Many2many('product.template',string="Yarn")

class PurchaseDia(models.Model):
	_name = 'purchase.dia'

	name = fields.Char("Dia",required = True)

class PurchaseSL(models.Model):
	_name = 'purchase.sl'

	name = fields.Char("SL",required = True)

class PurchaseGauge(models.Model):
	_name = 'purchase.gauge'

	name = fields.Char("Gauge",required = True)

class PurchaseNDL(models.Model):
	_name = 'purchase.ndl'

	name = fields.Char("NDL",required = True)

class PurchaseWidth(models.Model):
	_name = 'purchase.width'

	name = fields.Char("Width",required = True)

class PurchaseGSM(models.Model):
	_name = 'purchase.gsm'

	name = fields.Char("GSM",required = True)

class PurchaseProcess(models.Model):
	_name = 'purchase.process'

	name = fields.Char("Process",required = True)

class PurchaseOTM(models.Model):
	_name = 'purchase.otm'

	name = fields.Char("OTM",required = True)

class PurchasePrimary(models.Model):
	_name = 'purchase.primary'

	name = fields.Char("Primary",required = True)

class PurchaseSecondary(models.Model):
	_name = 'purchase.secondary'

	name = fields.Char("Secondary",required = True)

class PurchaseSubject(models.Model):
	_name = 'purchase.subject'

	name = fields.Char("Subject",required = True)

class PurchaseColor(models.Model):
	_name = 'purchase.color'

	name = fields.Char("Color",required = True)

class PurchaseBrnd(models.Model):
	_name = 'purchase.brand'

	name = fields.Char("Yarn Brand",required = True)

class PurchaseProdcutType(models.Model):
	_name = 'purchase.product.type'

	name = fields.Char("Product Type",required = True)

class PurchaseLot(models.Model):
	_name = 'purchase.lot'

	name = fields.Char("Lot",required = True)

class PurchaseProductionUnit(models.Model):
	_name = 'purchase.production.unit'

	name = fields.Char("Production Units",required = True)

class AccessoriesIssuance(models.Model):
	_name = 'purchase.access.issue'

	name = fields.Date("Date", required=True)
	wo = fields.Many2one('mrp.production',string="WO")
	unit = fields.Many2one('purchase.production.unit',string="Production Units")
	issue_Person = fields.Many2one('hr.employee', string="Issued Person")
	tree_link =fields.One2many('purchase.access.tree','access_tree')

	source_location = fields.Many2one('stock.location',string="Source Location")
	destination_location = fields.Many2one('stock.location',string="Destination Location")
	warehouse_id = fields.Many2one('stock.location',string="Warehouse")
	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")

	@api.multi
	def in_validate(self, vals):

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			# 'partner_id':self.issue_Person.id,
			'location_id': self.source_location.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.destination_location.id,
			'origin': 'Accessories Issuance',
		})

		for x in self.tree_link:
			create_inventory_lines = inventory_lines.create({
				'product_id': x.product_id.id,
				'product_uom_qty': x.qty,
				'product_uom': x.product_id.uom_id.id,
				'location_id': self.source_location.id,
				'picking_id': create_inventory.id,
				'name': "test",
				'location_dest_id': self.destination_location.id,
			})

class AccessoriesIssuanceTree(models.Model):
	_name = 'purchase.access.tree'

	product_id = fields.Many2one('product.product',string="Product",required=True)
	uom = fields.Many2one('product.uom',string="UOM")
	qty = fields.Float("Qty Issue")
	remark = fields.Char("Remarks")

	access_tree = fields.Many2one('purchase.access.issue')

	@api.onchange('product_id')
	def get_uom(self):
		self.uom = self.product_id.uom_id

class Fabric_Receiving_Wizard_Tree(models.Model):
	_name="fabric.wizard.tree"

	fr_won = fields.Many2one('mrp.production',string="W/O",required = True)
	fr_lot = fields.Many2one('purchase.lot',string="Lot No")
	fr_todo = fields.Float("To Do")
	fr_done = fields.Float("Done")
	fabric_tree = fields.Many2one("fabric.wizard.class")
	color = fields.Many2one('purchase.color',string="Color")
	yarn_count = fields.Many2one('product.product',"Yarn Count")

	@api.onchange('fr_done')
	def get_fab_done(self):
		recived = self.fr_done
		reciveable = self.fr_todo + (self.fr_todo*0.1)

		if recived > reciveable:
			self.fr_done = self.fr_todo
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Recived Quantity should not be greater than the Reciveable Quantity'}}

class Fabric_Receiving_Wizard(models.Model):
	_name = "fabric.wizard.class"
	_rec_name = 'id'

	fabric_link  = fields.One2many("fabric.wizard.tree","fabric_tree")
	get_list = fields.Boolean("Get List")
	l_list = fields.Boolean("L List")
	tree_id = fields.Integer("ID")
	date = fields.Date("Date" ,required=True)
	name = fields.Many2one('res.partner',string="Name")
	seq_code = fields.Char("Security Code")
	req_code = fields.Char("Requisition Code")

	source_location = fields.Many2one('stock.location',string="Source Location")
	destination_location = fields.Many2one('stock.location',string="Destination Location")
	warehouse_id = fields.Many2one('stock.location',string="Warehouse")
	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")

	@api.onchange('get_list')
	def get_lines(self):
 
		active_class = self.env['fabric.dyeing'].browse(self._context.get('active_id'))
		data = []
		t = 0.0
		if self.get_list == True:
			self.tree_id = active_class.id
			self.name = active_class.name
			for x in active_class.tree_link:
				if x.receive_qty > 0:
					t = x.receivable_qty - x.receive_qty
				else:
					t = x.receivable_qty
				data.append({
					'fr_won':x.won,
					'fr_lot':x.lot,
					'fr_todo':t,
					'color': x.color.id,
					'yarn_count': x.fabric.id,

					})
			self.fabric_link = data

	@api.multi
	def update(self):
		active_class = self.env['fabric.dyeing'].browse(self._context.get('active_id'))
		if active_class:
			self.tree_id = active_class.id
			for x in self.fabric_link:
				if x.fr_done > 0:
					for y in active_class.tree_link:
						if x.fr_won == y.won:
							y.receive_qty = x.fr_done + y.receive_qty
							self.l_list = 'True'

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.source_location.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.destination_location.id,
			'origin': 'Fabric Reciving',
		})

		for x in self.fabric_link:
			create_inventory_lines = inventory_lines.create({
				'product_id':x.yarn_count.id,
				'product_uom_qty':x.fr_done,
				'product_uom': x.yarn_count.uom_id.id,
				'location_id':15,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': 9,
				})

class Yarn_Receiving_Wizard_Tree(models.Model):
	_name="yarn.wizard.tree"

	fr_won = fields.Many2one('mrp.production',string="W/O",required = True)
	fr_lot = fields.Many2one('purchase.lot',string="Lot No")
	fr_todo = fields.Float("To Do")
	fr_done = fields.Float("Done")
	yarn_tree = fields.Many2one("yarn.wizard.class")
	color = fields.Many2one('purchase.color',string="Color")
	yarn_count = fields.Many2one('product.product',string="Yarn Count")

	@api.onchange('fr_done')
	def get_yarn_done(self):
		recived = self.fr_done
		reciveable = self.fr_todo + (self.fr_todo*0.1)

		if recived > reciveable:
			self.fr_done = self.fr_todo
			return {'value':{}, 'warning':{
			'title': 'Warning', 'message': 'Recived Quantity should not be greater than the Reciveable Quantity'}}

class Yarn_Receiving_Wizard(models.Model):
	_name = "yarn.wizard.class"
	_rec_name = 'id'

	yarn_link  = fields.One2many("yarn.wizard.tree","yarn_tree")
	get_list = fields.Boolean("Get List")
	l_list = fields.Boolean("L List")
	tree_id = fields.Integer("ID")
	date = fields.Date("Date" ,required=True)
	name = fields.Many2one('res.partner',string="Name")
	mf_no = fields.Char("MF No")
	seq_code = fields.Char("Security Code")
	req_code = fields.Char("Requisition Code")

	source_location = fields.Many2one('stock.location',string="Source Location")
	destination_location = fields.Many2one('stock.location',string="Destination Location")
	warehouse_id = fields.Many2one('stock.location',string="Warehouse")
	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")

	@api.onchange('get_list')
	def get_lines(self):
 
		active_class = self.env['yarn.dyeing'].browse(self._context.get('active_id'))
		data = []
		t = 0.0
		if self.get_list == True:
			self.tree_id = active_class.id
			self.name = active_class.name
			for x in active_class.tree_link:
				if x.receive_qty > 0:
					t = x.receiveable_qty - x.receive_qty
				else:
					t = x.receiveable_qty
				data.append({
					'fr_won':x.won,
					'fr_lot':x.lot,
					'fr_todo':t,
					'color':x.color.id,
					'yarn_count': x.yarn.id,
					})
			self.yarn_link = data

	@api.multi
	def update(self):
		active_class = self.env['yarn.dyeing'].browse(self._context.get('active_id'))
		if active_class:
			self.tree_id = active_class.id
			for x in self.yarn_link:
				if x.fr_done > 0:
					for y in active_class.tree_link:
						if x.fr_won == y.won:
							y.lot = x.fr_lot
							y.receive_qty = x.fr_done + y.receive_qty
							self.l_list = 'True'

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.source_location.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.destination_location.id,
			'origin': 'Yarn Reciving',
		})

		for x in self.yarn_link:
			create_inventory_lines = inventory_lines.create({
				'product_id':x.yarn_count.id,
				'product_uom_qty':x.fr_done,
				'product_uom': 1,
				'location_id':15,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': 9,
				})

class Knit_Receiving_Wizard_Tree(models.Model):
	_name="knit.wizard.tree"

	fr_won = fields.Many2one('mrp.production',string="W/O",required = True)
	fr_lot = fields.Many2one('purchase.lot',string="Lot No")
	fr_todo = fields.Float("To Do")
	fr_done = fields.Float("Done")
	knit_tree = fields.Many2one("knit.wizard.class")
	product = fields.Many2one('product.product',string="Product")

class Knit_Receiving_Wizard(models.Model):
	_name = "knit.wizard.class"
	_rec_name = 'id'

	knit_link  = fields.One2many("knit.wizard.tree","knit_tree")
	get_list = fields.Boolean("Get List")
	l_list = fields.Boolean("L List")
	tree_id = fields.Integer("ID")
	date = fields.Date("Date" ,required=True)
	name = fields.Many2one('res.partner',string="Name")

	source_location = fields.Many2one('stock.location',string="Source Location")
	destination_location = fields.Many2one('stock.location',string="Destination Location")
	warehouse_id = fields.Many2one('stock.location',string="Warehouse")
	picking_type_id = fields.Many2one('stock.picking.type',string="Picking Type")

	@api.onchange('get_list')
	def get_lines(self):
 
		active_class = self.env['fabric.knitting'].browse(self._context.get('active_id'))
		data = []
		t = 0.0
		if self.get_list == True:
			self.tree_id = active_class.id
			self.name = active_class.name
			for x in active_class.tree_link:
				if x.received > 0:
					t = x.required - x.received
				else:
					t = x.required
				data.append({
					'fr_won':x.won,
					'fr_lot':x.lot,
					'fr_todo':t,
					'product': x.yarn.id

					})
			self.knit_link = data

	@api.multi
	def update(self):
		active_class = self.env['fabric.knitting'].browse(self._context.get('active_id'))
		if active_class:
			self.tree_id = active_class.id
			for x in self.knit_link:
				if x.fr_done > 0:
					for y in active_class.tree_link:
						if x.fr_won == y.won:
							y.lot = x.fr_lot
							y.received = x.fr_done + y.received
							self.l_list = 'True'

		inventory = self.env['stock.picking']
		inventory_lines = self.env['stock.move'].search([])
		create_inventory = inventory.create({
			'partner_id':self.name.id,
			'location_id': self.source_location.id,
			'picking_type_id' : self.picking_type_id.id,
			'location_dest_id' : self.destination_location.id,
			'origin': 'Fabric Knitting Reciving',
		})

		for x in self.knit_link:
			create_inventory_lines = inventory_lines.create({
				'product_id':x.product.id,
				'product_uom_qty':x.fr_done,
				'product_uom': 1,
				'location_id':15,
				'picking_id': create_inventory.id,
				'name':"test",
				'location_dest_id': 9,
				})

class HrEmployeeForm(models.Model):
	_inherit = "hr.employee"

	merchant = fields.Boolean(string="Merchant")