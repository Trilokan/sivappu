# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ReportAsserts(models.TransientModel):
    _name = "report.stock.asserts"

    product_id = fields.Many2one(comodel_name="arc.product", string="Product", required=True)

    @api.multi
    def trigger_stock_asserts(self):
        recs = self.env["arc.asserts"].search([("product_id", "=", self.product_id.id)])

        report = []
        for rec in recs:
            report.append({"Product": rec.product_id.name,
                           "Manufacturer": rec.manufacturer,
                           "Manufacture Date": rec.manufactured_date,
                           "Expiry Date": rec.expiry_date,
                           "Serial No": rec.serial_no,
                           "Model No": rec.model_no,
                           "Warranty Date": rec.warranty_date,
                           "Order Date": rec.order_date,
                           "Purchase Date": rec.purchase_date,
                           "Vendor": rec.vendor_id.name,
                           "Working": rec.is_working,
                           "Condem": rec.is_condem})
