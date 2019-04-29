# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
ADJUST_TYPE = [("increase", "Increase"), ("decrease", "Decrease")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StockAdjustment(models.Model):
    _name = "stock.adjustment"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    adjusted_by = fields.Many2one(comodel_name="arc.person", string="Approve By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    adjust_type = fields.Selection(selection=ADJUST_TYPE, string="Adjust Type", default="increase", required=True)
    adjustment_detail = fields.One2many(comodel_name="stock.adjustment.detail", inverse_name="adjustment_id")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        writter = "Stock adjustment confirmed by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Store adjustment cancel by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "cancel", "writter": writter})

    def generate_move(self, recs):
        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])

        if self.adjust_type == "increase":
            source_id = config.adjustment_id.id
            destination_id = config.store_id.id

        elif self.adjust_type == "decrease":
            source_id = config.store_id.id
            destination_id = config.adjustment_id.id

        for rec in recs:
            result = {"source_id": source_id,
                      "destination_id": destination_id,
                      "reference": rec.name,
                      "product_id": rec.product_id.id,
                      "description": rec.description,
                      "quantity": rec.adjust_quantity,
                      "unit_price": rec.unit_price,
                      "progress": "moved"}

            self.env["arc.move"].create(result)

    @api.multi
    def trigger_approve(self):
        adjusted_by = self.env.user.person_id.id
        recs = self.env["stock.adjustment.detail"].search([("adjustment_id", "=", self.id), ("adjust_quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_move(recs)

        writter = "Stock adjustment by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "approved", "writter": writter, "adjusted_by": adjusted_by})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StockAdjustment, self).create(vals)


class StockAdjustmentDetail(models.Model):
    _name = "stock.adjustment.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="arc.product", string="Item", required=True)
    description = fields.Text(string="Item Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    adjust_quantity = fields.Float(string="Adjust Quantity", default=0, required=True)
    unit_price = fields.Float(string="Unit Price", default=0, required=True)
    comment = fields.Text(string="Comment")
    adjustment_id = fields.Many2one(comodel_name="stock.adjustment", string="Stock Adjustment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="adjustment_id.progress")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StockAdjustmentDetail, self).create(vals)
