# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class ReportStockStatement(models.TransientModel):
    _name = "report.stock.statement"

    from_date = fields.Date(string="Fom Date", required=True)
    till_date = fields.Date(string="Till Date", required=True)
    product_id = fields.Many2one(comodel_name="arc.product", string="Product")

    @api.multi
    def trigger_stock_evaluation(self):
        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])
        recs = self.env["arc.date.calendar"].date_array(self.from_date, self.till_date)

        report = []

        report_data = {"Name": self.product_id.name,
                       "Code": self.product_id.product_uid,
                       "UOM": self.product_id.uom_id.name,
                       "Product Group": self.product_id.product_group_id.name,
                       "Product Sub Group": self.product_id.sub_group_id.name,
                       "HSN Code": self.product_id.hsn_code,
                       "Description": self.product_id.description,
                       "Category": self.product_id.category_id.name}
        for rec in recs:
            date_obj = datetime.strptime(rec, "%Y-%m-%d")
            opening_date_obj = date_obj - timedelta(days=1)
            opening_date = opening_date_obj.strftime("%Y-%m-%d")
            closing_date = rec

            opening = self.env["arc.stock"].get_current_stock_date(rec.id, config.store_id.id, opening_date)
            closing = self.env["arc.stock"].get_current_stock_date(rec.id, config.store_id.id, closing_date)

            rec_data = report_data.update({"Date": rec,
                                           "Opening Quantity": opening,
                                           "Closing Quantity": closing})
            report.append(rec_data)

        print report

