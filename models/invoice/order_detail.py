# -*- coding: utf-8 -*-

from odoo import models, fields, api

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved")]


class OrderDetail(models.Model):
    _name = "order.detail"

    quotation_ref = fields.Char(string="Quotation Ref")
    name = fields.Char(string="Name")
    product_id = fields.Many2one(comodel_name="arc.product", string="Product", required=True)
    description = fields.Text(string="Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Float(string="Quantity", required=True, default=0.0)
    unit_price = fields.Float(string="Unit Price", required=True, default=0.0)
    discount = fields.Float(string="Discount", required=True, default=0.0)
    tax_id = fields.Many2one(comodel_name="product.tax", string="Tax", required=True)
    pf = fields.Float(string="PF", required=True, default=0.0)
    discount_amount = fields.Float(string="", required=True, readonly=True, default=0.0)
    after_discount = fields.Float(string="", required=True, readonly=True, default=0.0)
    tax_amount = fields.Float(string="", required=True, default=0.0)
    cgst = fields.Float(string="CGST", required=True, readonly=True, default=0.0)
    sgst = fields.Float(string="SGST", required=True, readonly=True, default=0.0)
    igst = fields.Float(string="IGST", required=True, readonly=True, default=0.0)
    total = fields.Float(string="Total", required=True, readonly=True, default=0.0)
    order_id = fields.Many2one(comodel_name="arc.order", string="Order")
    progress = fields.Selection(selection=PROGRESS_INFO,  string="Progress", related="order_id.progress")

    def update_total(self):
        state = self.order_id.person_id.state_id.id

        if state == self.env.user.company_id.state_id.id:
            state_type = "inter"
        else:
            state_type = "outer"

        vals = self.env["arc.calculation"].get_item_val(self.unit_price,
                                                        self.quantity,
                                                        self.discount,
                                                        self.pf,
                                                        self.tax_id.rate,
                                                        state_type)

        self.write(vals)

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(OrderDetail, self).create(vals)
