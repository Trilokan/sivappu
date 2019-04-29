# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("approved", "Approved"), ("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class AssertsCapitalisation(models.Model):
    _name = "asserts.capitalisation"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    approved_by = fields.Many2one(comodel_name="arc.person", string="Approve By", readonly=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    # order_id = fields.Many2one(comodel_name="purchase.order", string="Purchase Order")
    # invoice_id = fields.Many2one(comodel_name="purchase.invoice", string="Purchase Invoice")
    product_id = fields.Many2one(comodel_name="arc.product", string="Product", required=True)
    description = fields.Text(string="Description")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    quantity = fields.Integer(string="Quantity", default=0, required=True)
    asserts_ids = fields.One2many(comodel_name="arc.asserts", inverse_name="capitalise_id")
    comment = fields.Text(string="Comment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Char(string="Writter", track_visibility="always")

    _sql_constraints = [('quantity_check', 'CHECK(quantity > 1)', 'Check Assert Quantity')]

    def generate_stock_move(self):
        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])
        source_id = config.store_id.id
        destination_id = config.assert_id.id

        result = {"source_id": source_id,
                  "destination_id": destination_id,
                  "reference": self.name,
                  "product_id": self.product_id.id,
                  "description": self.description,
                  "quantity": self.quantity,
                  "progress": "moved"}

        self.env["arc.move"].create(result)

    def capitalise(self):
        quantities = self.quantity
        for quantity in range(0, quantities):
            data = {"product_id": self.product_id.id,
                    "capitalise_id": self.id}
            self.env["arc.asserts"].create(data)

    @api.multi
    def trigger_approve(self):
        self.generate_stock_move()
        self.capitalise()
        writter = "Asserts capitalised by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "approved", "writter": writter})

    @api.multi
    def trigger_confirm(self):
        writter = "Asserts capitalisation confirmed by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Asserts capitalisation cancel by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "cancel", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(AssertsCapitalisation, self).create(vals)
