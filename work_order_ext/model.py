# -*- coding: utf-8 -*- 
from odoo import models, fields, api
import random

class WokrOrderMain(models.Model):
    _inherit = 'mrp.production'
    _rec_name = 'order_name'

    custome_po = fields.Char(string="Customer Po#")
    style_no = fields.Many2one('style.number',string="Style No")
    vessal = fields.Date(string="Vessal Date")
    delivery = fields.Date(string="Delivery Date")
    plan_qty = fields.Char(string="Plan Qty")
    week = fields.Integer(string="Week")
    order_name = fields.Char(string="Workorder Name")

    remarks = fields.Text(string="Remarks")

    destination = fields.Many2one('country.countries',string="Destination")
    unit = fields.Many2one('purchase.access.issue',string="Unit")
    buyer = fields.Many2one('res.partner',string="Buyer")
    production_id =fields.One2many('production.tree','production_tree')

    state = fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('inprogress','InProgress'),
        ('done','Done'),
        ('cancel','Cancel'),
        ],default='draft')
                        
    @api.multi
    def in_draft(self):
        self.state = "draft"
                        
    @api.multi
    def in_confirmed(self):
        self.state = "confirmed"
                        
    @api.multi
    def in_progress(self):
        self.state = "inprogress"
                        
    @api.multi
    def in_done(self):
        self.state = "done"
                        
    @api.multi
    def in_cancel(self):
        self.state = "cancel"

    @api.multi
    def validate_tree(self):
        p_order = self.env['purchase.order'].search([('wo_no.name','=',self.name)])
        for x in self.production_id:
            ordered_qty = x.purchased
            for z in p_order:
                for y in z.order_line2:
                    if y.product_id.id == x.accessories.id:
                        ordered_qty = ordered_qty + y.product_qty
            x.purchased = ordered_qty

        for x in self.production_id:
            stock = self.env['stock.move'].search([('product_id.id','=',x.accessories.id)])
            ordered_qty_stock = 0
            for z in stock:
                ordered_qty_stock = ordered_qty_stock + z.product_uom_qty
            x.in_stock = ordered_qty_stock

        for x in self.production_id:
            accsss_issue = self.env['purchase.access.issue'].search([('wo.id','=',self.id)])
            issuesd_qty = 0
            for z in accsss_issue:
                for y in z.tree_link:
                    if y.product_id.id == x.accessories.id:
                        issuesd_qty = issuesd_qty + y.qty
            x.issued = issuesd_qty


        for x in self.production_id:
            x.remaining = x.in_stock - x.issued

    @api.model
    def create(self, vals):
        new_record = super(WokrOrderMain, self).create(vals)

        m_orders = self.env['mrp.production'].search([("style_no.id","=",new_record.style_no.id)])
        if len(m_orders) > 1:
            rand = m_orders[0]
            split_rand = rand.name.split(' - ')
            m_name = split_rand[0]

            record = len(m_orders)
            list_1 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

            req_record = 0
            if record >= 28 :
                req_record = (record%28)
                req_phase = int(record/28)
                addition = m_name + ' - ' + list_1[req_record]

                for x in range(0, req_phase):
                    addition = addition + list_1[req_record]

            else:
                req_record = record - 2
                addition = m_name + ' - ' + list_1[(req_record)]

            new_record.name = addition

        return new_record

class WokrOrder(models.Model):
    _name = 'production.tree'

    accessories = fields.Many2one('product.product',string="Accessories")
    required_quantity = fields.Float(string="Required Quantity")
    purchased = fields.Float(string="Purchased")
    in_stock = fields.Float(string="In Stock")
    issued = fields.Float(string="Issued")
    remaining = fields.Float(string="Remaining")
    uom = fields.Many2one('product.uom',string="UOM")
    factor = fields.Float(string="Factor")
    source = fields.Selection([
        ('imp','IMP'),
        ('local','Local')
        ],string="Source")

    production_tree  =fields.Many2one('mrp.production')

    @api.onchange('accessories')
    def onchange_depart(self):
        self.uom = self.accessories.uom_id.id

class Countries(models.Model):
    _name = 'country.countries'
    _rec_name = 'country'

    country = fields.Char(string="Name")

class Style_no(models.Model):
    _name = "style.number"
    _rec_name = 'name'

    name = fields.Char(string="Name")