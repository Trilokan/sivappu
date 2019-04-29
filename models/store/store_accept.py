# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("accepted", "Accepted"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreAccept(models.Model):
    _name = "store.accept"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    return_id = fields.Many2one(comodel_name="store.return", string="Return", required=True)
    accept_by = fields.Many2one(comodel_name="arc.person", string="Accept By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    accept_detail = fields.One2many(comodel_name="store.accept.detail", inverse_name="accept_id", string="Accept Detail")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_cancel(self):
        writter = "Store accept cancel by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "cancel", "writter": writter})

    def generate_move(self, recs):
        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])

        source_id = self.department_id.location_id.id
        destination_id = config.store_id.id

        for rec in recs:
            result = {"source_id": source_id,
                      "destination_id": destination_id,
                      "reference": rec.name,
                      "product_id": rec.product_id.id,
                      "description": rec.description,
                      "quantity": rec.accept_quantity,
                      "progress": "moved"}

            self.env["arc.move"].create(result)

    @api.multi
    def trigger_accept(self):
        accept_by = self.env.user.person_id.id
        recs = self.env["store.accept.detail"].search([("accept_id", "=", self.id), ("accept_quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_move(recs)

        writter = "Stock accepted by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "accepted", "writter": writter, "accept_by": accept_by})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StoreAccept, self).create(vals)


class StoreAcceptDetail(models.Model):
    _name = "store.accept.detail"

    name = fields.Char(string="Name", readonly=True)
    reference = fields.Char(string="Reference", readonly=True)
    product_id = fields.Many2one(comodel_name="arc.product", string="Product", required=True)
    description = fields.Text(string="Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    returned_quantity = fields.Float(string="Return Quantity", default=0, required=True)
    accept_quantity = fields.Float(string="Accepting Quantity", default=0, required=True)
    accept_id = fields.Many2one(comodel_name="store.accept", string="Store Accept")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="accept_id.progress")

    @api.constrains("quantity")
    def check_issue_quantity(self):
        if self.accept_quantity > self.returned_quantity:
            raise exceptions.ValidationError("Error! Accepted quantity more than return quantity")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StoreAcceptDetail, self).create(vals)
