# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("issued", "Issued"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class StoreIssue(models.Model):
    _name = "store.issue"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    request_id = fields.Many2one(comodel_name="store.request", string="Request", required=True)
    issue_by = fields.Many2one(comodel_name="arc.person", string="Issue By", readonly=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    issue_detail = fields.One2many(comodel_name="store.issue.detail", inverse_name="issue_id", string="Issue Detail")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_cancel(self):
        writter = "Store issue cancel by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "cancel", "writter": writter})

    def generate_move(self, recs):
        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])

        source_id = config.store_id.id
        destination_id = self.department_id.location_id.id

        for rec in recs:
            result = {"source_id": source_id,
                      "destination_id": destination_id,
                      "reference": rec.name,
                      "product_id": rec.product_id.id,
                      "description": rec.description,
                      "quantity": rec.issue_quantity,
                      "progress": "moved"}

            self.env["arc.move"].create(result)

    @api.multi
    def trigger_issue(self):
        issue_by = self.env.user.person_id.id
        recs = self.env["store.issue.detail"].search([("issue_id", "=", self.id), ("issue_quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_move(recs)

        writter = "Stock issued by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "issued", "writter": writter, "issue_by": issue_by})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StoreIssue, self).create(vals)


class StoreIssueDetail(models.Model):
    _name = "store.issue.detail"

    name = fields.Char(string="Name", readonly=True)
    reference = fields.Char(string="Reference", readonly=True)
    product_id = fields.Many2one(comodel_name="arc.product", string="Item", required=True)
    description = fields.Text(string="Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    requested_quantity = fields.Float(string="Requested Quantity", default=0, required=True)
    issue_quantity = fields.Float(string="Issue Quantity", default=0, required=True)
    issue_id = fields.Many2one(comodel_name="store.issue", string="Store Issue")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="issue_id.progress")

    @api.constrains("issue_quantity")
    def check_issue_quantity(self):
        if self.issue_quantity > self.requested_quantity:
            raise exceptions.ValidationError("Error! Issue quantity more than requested")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(StoreIssueDetail, self).create(vals)
