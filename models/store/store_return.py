# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreReturn(models.Model):
    _name = "store.return"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    returned_by = fields.Many2one(comodel_name="arc.person", string="Returned By", readonly=True)
    approved_by = fields.Many2one(comodel_name="arc.person", string="Approved By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    return_detail = fields.One2many(comodel_name="store.return.detail", inverse_name="return_id", string="Return Detail")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        returned_by = self.env.user.person_id.id
        writter = "Store Return Confirmed by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "confirmed", "writter": writter, "returned_by": returned_by})

    @api.multi
    def trigger_cancel(self):
        cancel_by = self.env.user.person_id.id
        writter = "Store Return cancel by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "cancel", "writter": writter, "approved_by": cancel_by})

    def generate_accept(self, recs):
        accept_detail = []
        for rec in recs:
            accept_detail.append((0, 0, {"reference": rec.name,
                                         "product_id": rec.product_id.id,
                                         "description": rec.description,
                                         "returned_quantity": rec.approved_quantity}))

        if accept_detail:
            accept = {"return_id": self.id,
                      "department_id": self.department_id.id,
                      "accept_detail": accept_detail}

            self.env["store.accept"].create(accept)

    @api.multi
    def trigger_approve(self):
        approved_by = self.env.user.person_id.id
        recs = self.env["store.return.detail"].search([("return_id", "=", self.id), ("approved_quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_accept(recs)

        writter = "Store Return Approved by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "approved", "writter": writter, "approved_by": approved_by})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StoreReturn, self).create(vals)


class StoreReturnDetail(models.Model):
    _name = "store.return.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="arc.product", string="Item", required=True)
    description = fields.Text(string="Item Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    returned_quantity = fields.Float(string="Return Quantity", default=0, required=True)
    approved_quantity = fields.Float(string="Approved Quantity", default=0, required=True)
    return_id = fields.Many2one(comodel_name="store.return", string="Store Return")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="return_id.progress")

    @api.constrains("returned_quantity")
    def check_requested_quantity(self):
        if self.approved_quantity > self.returned_quantity:
            raise exceptions.ValidationError("Error! Approved quantity more than return quantity")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StoreReturnDetail, self).create(vals)
