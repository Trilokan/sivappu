# -*- coding: utf-8 -*-

from odoo import models, fields, api

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved")]


class InvoiceDetail(models.Model):
    _name = "invoice.detail"

    order_ref = fields.Char(string="Order Reference")
    material_ref = fields.Char(string="Material Reference")
    name = fields.Char(string="Name")
    product_id = fields.Many2one(comodel_name="arc.product", string="Product")
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
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")
    progress = fields.Selection(selection=PROGRESS_INFO,  string="Progress", related="invoice_id.progress")

    def update_total(self):
        state = self.invoice_id.person_id.state_id.id

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
        return super(InvoiceDetail, self).create(vals)
