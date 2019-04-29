# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class ReportStockMovement(models.TransientModel):
    _name = "report.stock.movement"

    from_date = fields.Date(string="Fom Date", required=True)
    till_date = fields.Date(string="Till Date", required=True)
    product_id = fields.Many2one(comodel_name="arc.product", string="Product", required=True)

    @api.multi
    def trigger_stock_movement(self):
        date_obj = datetime.strptime(self.from_date, "%Y-%m-%d")
        opening_date = date_obj - timedelta(days=1)
        closing_date = self.till_date

        recs = self.env["arc.move"].search([("date", ">=", opening_date),
                                            ("date", "<=", closing_date),
                                            ("product_id", "=", self.product_id.id),
                                            ("progress", "=", "moved")])

        report = []
        for rec in recs:
            report.append({"Date": rec.date,
                           "Name": rec.name,
                           "Product": rec.product_id.name,
                           "Description": rec.description,
                           "UOM": rec.uom_id.name,
                           "Source Location": rec.source_id.location_uid,
                           "Destination Location": rec.destination_id.location_uid,
                           "Quantity": rec.quantity})

        print report
