# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class ReportStockEvaluation(models.TransientModel):
    _name = "report.stock.evaluation"

    from_date = fields.Date(string="Fom Date", required=True)
    till_date = fields.Date(string="Till Date", required=True)
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
    def trigger_stock_evaluation(self):
        recs = self.get_records()

        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])
        date_obj = datetime.strptime(self.from_date, "%Y-%m-%d")
        opening_date = date_obj - timedelta(days=1)
        closing_date = self.till_date

        report = []
        for rec in recs:
            opening = self.env["arc.stock"].get_current_stock_date(rec.id, config.store_id.id, opening_date)
            closing = self.env["arc.stock"].get_current_stock_date(rec.id, config.store_id.id, closing_date)
            report.append({"Name": rec.name,
                           "Code": rec.product_uid,
                           "UOM": rec.uom_id.name,
                           "Product Group": rec.product_group_id.name,
                           "Product Sub Group": rec.sub_group_id.name,
                           "HSN Code": rec.hsn_code,
                           "Description": rec.description,
                           "Category": rec.category_id.name,
                           "Opening Quantity": opening,
                           "Closing Quantity": closing})

        print report

