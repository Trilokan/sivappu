# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VendorSelection(models.Model):
    _name = "vendor.selection"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name", readonly=True)
    vs_detail = fields.One2many(comodel_name="vendor.selection.detail", inverse_name="vs_id")

    @api.multi
    def trigger_generate_quote(self):
        recs = self.vs_detail

        for rec in recs:
            for person_id in rec.person_ids:
                quote_id = self.env["purchase.quotation"].search([("vs_id", "=", self.id),
                                                                  ("person_id", "=", person_id.id)])

                if not quote_id:
                    quote_id = self.env["purchase.quotation"].create({"person_id": person_id.id, "vs_id": self.id})

                quote_detail_id = self.env["quotation.detail"].search([("quotation_id", "=", quote_id.id),
                                                                         ("vs_detail_id", "=", rec.id)])

                if not quote_detail_id:
                    quote_detail_id = self.env["quotation.detail"].create({"vs_detail_id": rec.id,
                                                                           "quotation_id": quote_id.id,
                                                                           "product_id": rec.product_id.id,
                                                                           "description": rec.description,
                                                                           "quantity": rec.quantity})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(VendorSelection, self).create(vals)


class VendorSelectionDetail(models.Model):
    _name = "vendor.selection.detail"

    product_id = fields.Many2one(comodel_name="arc.product", string="Product")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    description = fields.Text(string="Description", required=True)
    quantity = fields.Float(string="Quantity", default=0.0, required=True)
    comment = fields.Text(string="Comment")
    ref = fields.Char(string="ref")
    person_ids = fields.Many2many(comodel_name="arc.person", string="Vendor(s)")
    vs_id = fields.Many2one(comodel_name="vendor.selection", string="Vendor Selection")
    quotation_detail = fields.One2many(comodel_name="quotation.detail", inverse_name="vs_detail_id")
    price_ids = fields.One2many(comodel_name="vendor.selection.price", inverse_name="vs_detail_id", readonly=True)


class VendorSelectionDetailPrice(models.Model):
    _name = "vendor.selection.price"

    date = fields.Date(string="Date", readonly=True)
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice", readonly=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Vendor", readonly=True)
    description = fields.Text(string="Description", readonly=True)
    unit_price = fields.Float(string="Unit Price", default=0.0, readonly=True)
    quantity = fields.Float(string="Quantity", default=0.0, readonly=True)
    discount = fields.Float(string="Discount", default=0.0, readonly=True)
    pf = fields.Float(string="PF", default=0.0, readonly=True)
    tax_id = fields.Many2one(comodel_name="product.tax", string="Tax", readonly=True)
    total = fields.Float(string="Total", default=0.0, readonly=True)
    vs_detail_id = fields.Many2one(comodel_name="vendor.selection.detail", string="Vendor Selection", readonly=True)
