# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ReportCurrentStock(models.TransientModel):
    _name = "report.current.stock"

    product_ids = fields.Many2many(comodel_name="arc.product", string="Product(s)")

    def get_records(self):
        records = []

        for rec in self.product_ids:
            records.append(rec.id)

        if records:
            domain = [("id", "in", records)]
        else:
            domain = []

        recs = self.env["arc.product"].search(domain)

        return recs

    @api.multi
    def trigger_current_stock(self):
        recs = self.get_records()

        report = []
        for rec in recs:

            report.append({"Name": rec.name,
                           "Code": rec.product_uid,
                           "UOM": rec.uom_id.name,
                           "Product Group": rec.product_group_id.name,
                           "Product Sub Group": rec.sub_group_id.name,
                           "HSN Code": rec.hsn_code,
                           "Description": rec.description,
                           "Category": rec.category_id.name,
                           "Quantity": rec.stock_count})

        print report


