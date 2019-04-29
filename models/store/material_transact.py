# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

TRANSACT_TYPE = [("in", "In"), ("out", "Out")]
PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class MaterialTransact(models.Model):
    _name = "material.transact"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Person", required=True)
    order_id = fields.Many2one(comodel_name="arc.order", string="Order", required=True)
    # pharmacy_id = fields.Many2one(comodel_name="arc.pharmacy", string="Pharmacy", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    transact_by = fields.Many2one(comodel_name="arc.person", string="Transact By")
    transact_on = fields.Date(string="Transact On")
    transact_type = fields.Selection(selection=TRANSACT_TYPE, string="Transact Type", required=True)
    transact_detail = fields.One2many(comodel_name="transact.detail", inverse_name="transact_id")
    comment = fields.Text(string="Comment")
    is_invoice_generated = fields.Boolean(string="Is Invoice Generated")
    writter = fields.Text(string="Writter", track_visibility="always")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    def get_transact_parent(self, rec):
        order_id = self.env["order.detail"].search([("name", "=", rec.ref)])

        if not order_id:
            raise exceptions.ValidationError("Error! Order is not found")

        return order_id

    def get_payment_type(self):
        payment_type = False
        order_type = self.order_id.order_type

        if order_type in ["purchase", "sale_return"]:
            payment_type = "payable"
        elif order_type in ["purchase_return", "sale"]:
            payment_type = "receivable"

        if not payment_type:
            raise exceptions.ValidationError("Error! Payment Type is not found")

        return payment_type

    @api.multi
    def trigger_generate_invoice(self):
        recs = self.env["transact.detail"].search([("transact_id", "=", self.id), ("quantity", ">", 0)])

        invoice_detail = []
        for rec in recs:
            record_id = self.get_transact_parent(rec)
            invoice_detail.append((0, 0, {"product_id": rec.product_id.id,
                                          "description": rec.description,
                                          "quantity": rec.quantity,
                                          "pf": record_id.pf,
                                          "discount": record_id.discount,
                                          "tax_id": record_id.tax_id.id,
                                          "unit_price": record_id.unit_price}))

        self.env["arc.invoice"].create({"person_id": self.person_id.id,
                                        "order_id": self.order_id.id,
                                        "invoice_type": self.order_id.order_type,
                                        "payment_type": self.get_payment_type(),
                                        "invoice_detail": invoice_detail})

    @api.multi
    def generate_balance(self):
        recs = self.transact_detail

        transact_detail = []

        for rec in recs:
            if rec.request_quantity - (rec.received_quantity + rec.quantity):
                transact_detail.append((0, 0, {"ref": rec.ref,
                                               "product_id": rec.product_id.id,
                                               "description": rec.description,
                                               "request_quantity": rec.request_quantity,
                                               "received_quantity": rec.received_quantity + rec.quantity}))

        if transact_detail:
            self.env["material.transact"].create({"order_id": self.order_id.id,
                                                  "person_id": self.person_id.id,
                                                  "transact_type": self.transact_type,
                                                  "transact_detail": transact_detail})

    def generate_move(self, recs):
        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])

        if self.transact_type == "in":
            source_id = config.purchase_id.id
            destination_id = config.store_id.id
        elif self.transact_type == "out":
            source_id = config.store_id.id
            destination_id = config.purchase_id.id

        for rec in recs:
            result = {"source_id": source_id,
                      "destination_id": destination_id,
                      "reference": rec.name,
                      "product_id": rec.product_id.id,
                      "description": rec.description,
                      "quantity": rec.quantity,
                      "progress": "moved"}

            self.env["arc.move"].create(result)

    @api.multi
    def trigger_moved(self):
        recs = self.env["transact.detail"].search([("transact_id", "=", self.id), ("quantity", ">", 0)])

        if not recs:
            raise exceptions.ValidationError("Error! No Products found")

        self.generate_move(recs)
        self.generate_balance()
        writter = "Material Moved by {0} on {1}".format(self.env.user.name, CURRENT_INDIA)
        data = {"progress": "moved", "writter": writter}

        self.write(data)

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(MaterialTransact, self).create(vals)


class MaterialTransactDetail(models.Model):
    _name = "transact.detail"

    name = fields.Char(string="Name", readonly=True)
    product_id = fields.Many2one(comodel_name="arc.product", string="Product", readonly=True)
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", related="product_id.uom_id")
    description = fields.Text(string="Description", readonly=True)
    request_quantity = fields.Float(string="Request Quantity", default=0.0, readonly=True)
    received_quantity = fields.Float(string="Received Quantity", default=0.0, readonly=True)
    quantity = fields.Float(string="Receiving Quantity", default=0.0, required=True)
    transact_id = fields.Many2one(comodel_name="material.transact", string="Material Transact")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="transact_id.progress")
    ref = fields.Char(string="Reference")

    @api.constrains('quantity')
    def check_quantity(self):
        if (self.received_quantity + self.quantity) > self.request_quantity:
            raise exceptions.ValidationError("Error! Transact Quantity is more than requested")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(MaterialTransactDetail, self).create(vals)
