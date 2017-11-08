# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class WokrOrder(models.Model):
    _inherit = 'mrp.production'

    custome_po = fields.Char(string="Customer Po#")
    style_no = fields.Char(string="Style No")
    vessal = fields.Date(string="Vessal Date")
    plan_qty = fields.Char(string="Plan Qty")
    week = fields.Integer(string="Week")

    remarks = fields.Text(string="Remarks")

    destination = fields.Many2one('country.countries',string="Destination")
    unit = fields.Many2one('purchase.access.issue',string="Unit")
    buyer = fields.Many2one('res.partner',string="Buyer")
    production_id =fields.One2many('production.tree','production_tree')

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
        

class WokrOrder(models.Model):
    _name = 'production.tree'

    accessories = fields.Many2one('product.product',string="Accessories")
    required_quantity = fields.Float(string="Required Quantity")
    purchased = fields.Float(string="Purchased")
    in_stock = fields.Float(string="In Stock")
    issued = fields.Float(string="Issued")
    remaining = fields.Float(string="Remaining")

    production_tree  =fields.Many2one('mrp.production')

class Countries(models.Model):
    _name = 'country.countries'
    _rec_name = 'country'

    country = fields.Char(string="Name")