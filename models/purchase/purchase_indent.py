# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

INDENT_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]
APPROVAL_INFO = [("draft", "Draft"), ("approved", "Approved")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class PurchaseIndent(models.Model):
    _name = "purchase.indent"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    department_id = fields.Many2one(comodel_name="hr.department", required=True)
    request_by = fields.Many2one(comodel_name="arc.person", string="Request By", readonly=True)
    request_on = fields.Date(string="Request On", readonly=True)
    progress = fields.Selection(selection=INDENT_INFO, default="draft", string="Progress")
    indent_detail = fields.One2many(comodel_name="indent.detail", inverse_name="indent_id")
    comment = fields.Text(string="Comment")
    writter = fields.Text(string="Writter", track_visisbility="always")

    @api.multi
    def trigger_confirm(self):
        writter = "Purchase Indent confirmed by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"progress": "confirmed",
                    "writter": writter,
                    "request_by": self.env.user.person_id.id,
                    "request_on": CURRENT_DATE})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(PurchaseIndent, self).create(vals)


class PurchaseIndentDetail(models.Model):
    _name = "indent.detail"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="arc.product", string="Product", required=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    description = fields.Text(string="Description", required=True)
    request_quantity = fields.Float(string="Request Quantity", default=0.0, required=True)
    approved_quantity = fields.Float(string="Approved Quantity", default=0.0, required=True)
    approved_by = fields.Many2one(comodel_name="arc.person", string="Approved By", readonly=True)
    approved_on = fields.Date(string="Approved On", readonly=True)
    comment = fields.Text(string="Comment")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    indent_id = fields.Many2one(comodel_name="purchase.indent", string="Purchase Indent")
    indent_progress = fields.Selection(selection=INDENT_INFO, string="Progress", related="indent_id.progress")
    approval_progress = fields.Selection(selection=APPROVAL_INFO, string="Progress", default="draft")

    @api.constrains("request_quantity")
    def check_request_quantity(self):
        if self.request_quantity <= 0:
            raise exceptions.ValidationError("Error! Need Request quantity")

    @api.multi
    def trigger_approve(self):
        writter = "Indent Approved by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        self.write({"approval_progress": "approved",
                    "writter": writter,
                    "approved_by": self.env.user.person_id.id,
                    "approved_on": CURRENT_DATE})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(PurchaseIndentDetail, self).create(vals)
