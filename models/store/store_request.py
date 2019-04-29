# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreRequest(models.Model):
    _name = "store.request"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    request_detail = fields.One2many(comodel_name="store.request.detail", inverse_name="request_id")
    requested_by = fields.Many2one(comodel_name="arc.person", string="Requested By", readonly=True)
    approved_by = fields.Many2one(comodel_name="arc.person", string="Approved By", readonly=True)
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        requested_by = self.env.user.person_id.id
        writter = "Store Request Confirmed by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "confirmed", "writter": writter, "requested_by": requested_by})

    @api.multi
    def trigger_cancel(self):
        cancel_by = self.env.user.person_id.id
        writter = "Store Request cancel by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "cancel", "writter": writter, "approved_by": cancel_by})

    def generate_issue(self, recs):
        issue_detail = []
        for rec in recs:
            issue_detail.append((0, 0, {"reference": rec.name,
                                        "product_id": rec.product_id.id,
                                        "description": rec.description,
                                        "requested_quantity": rec.approved_quantity}))

        if issue_detail:
            issue = {"request_id": self.id,
                     "department_id": self.department_id.id,
                     "issue_detail": issue_detail}

            self.env["store.issue"].create(issue)

    @api.multi
    def trigger_approve(self):
        approved_by = self.env.user.person_id.id
        recs = self.env["store.request.detail"].search([("request_id", "=", self.id), ("approved_quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_issue(recs)

        writter = "Store Request Approved by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "approved", "writter": writter, "approved_by": approved_by})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StoreRequest, self).create(vals)


class StoreRequestDetail(models.Model):
    _name = "store.request.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="arc.product", string="Item", required=True)
    description = fields.Text(string="Item Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    requested_quantity = fields.Float(string="Request Quantity", default=0, required=True)
    approved_quantity = fields.Float(string="Approved Quantity", default=0, required=True)
    request_id = fields.Many2one(comodel_name="store.request", string="Store Request")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="request_id.progress")

    @api.constrains("approved_quantity")
    def check_requested_quantity(self):
        if self.approved_quantity > self.requested_quantity:
            raise exceptions.ValidationError("Error! Approved quantity more than requested")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StoreRequestDetail, self).create(vals)
