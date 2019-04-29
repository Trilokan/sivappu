# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

INVOICE_TYPE = [("sale", "Sales"),
                ("purchase", "Purchase"),
                ("sale_return", "Sales Return"),
                ("purchase_return", "Purchase Return")]
PROGRESS_INFO = [("draft", "Draft"),
                 ("confirmed", "Confirmed"),
                 ("approved", "Approved"),
                 ("cancel", "Cancel")]
PAYMENT_TYPE = [("payable", "Payable"), ("receivable", "Receivable")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class Quotation(models.Model):
    _name = "purchase.quotation"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    vs_id = fields.Many2one(comodel_name="vendor.selection", string="Vendor Selection")
    person_id = fields.Many2one(comodel_name="arc.person", string="Person", required=True)
    vendor_ref = fields.Char(string="Vendor Ref")
    quotation_detail = fields.One2many(comodel_name="quotation.detail", inverse_name="quotation_id")
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft")

    # Calculation
    sub_total_amount = fields.Float(string="Sub Total", required=True, readonly=True, default=0.0)
    others = fields.Float(string="Others", required=True, readonly=True, default=0.0)
    round_off = fields.Float(string="Rounding-Off", required=True, readonly=True, default=0.0)
    grand_amount = fields.Float(string="Grand Total", required=True, readonly=True, default=0.0)
    cgst = fields.Float(string="CGST", required=True, readonly=True, default=0.0)
    sgst = fields.Float(string="SGST", required=True, readonly=True, default=0.0)
    igst = fields.Float(string="IGST", required=True, readonly=True, default=0.0)
    tax_amount = fields.Float(string="Tax Amount", required=True, readonly=True, default=0.0)
    un_tax_amount = fields.Float(string="Un-Tax Amount", required=True, readonly=True, default=0.0)
    discount_amount = fields.Float(string="Discount Amount", required=True, readonly=True, default=0.0)
    pf = fields.Float(string="PF Amount", required=True, readonly=True, default=0.0)

    expected_delivery = fields.Char(string='Expected Delivery')
    freight = fields.Char(string='Freight')
    payment = fields.Char(string='Payment')
    insurance = fields.Char(string='Insurance')
    certificate = fields.Char(string='Certificate')
    warranty = fields.Char(string='Warranty')

    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    comment = fields.Text(string="Comment")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def generate_purchase_order(self):
        order_detail = []

        recs = self.env["quotation.detail"].search([("quotation_id", "=", self.id), ("quantity", ">", 0)])

        for rec in recs:
            order_detail.append((0, 0, {"quotation_ref": rec.name,
                                        "product_id": rec.product_id.id,
                                        "description": rec.description,
                                        "quantity": rec.quantity,
                                        "unit_price": rec.unit_price,
                                        "discount": rec.discount,
                                        "tax_id": rec.tax_id.id,
                                        "pf": rec.pf}))

        self.env["arc.order"].create({"vs_id": self.vs_id.id,
                                           "quotation_id": self.id,
                                           "person_id": self.person_id.id,
                                           "order_type": "purchase",
                                           "order_detail": order_detail})

    @api.multi
    def trigger_confirm(self):
        self.trigger_update_total()
        writter = "Quotation confirmed by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "confirmed", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_cancel(self):
        self.trigger_update_total()
        writter = "Quotation cancelled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "cancel", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_approve(self):
        self.trigger_update_total()
        self.generate_purchase_order()
        writter = "Quotation approved by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "approved", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_update_total(self):
        recs = self.quotation_detail

        sub_total_amount = cgst = sgst = igst = tax_amount = pf = discount_amount = 0
        for rec in recs:
            rec.update_total()
            cgst = cgst + rec.cgst
            sgst = sgst + rec.sgst
            igst = igst + rec.igst
            sub_total_amount = sub_total_amount + rec.total
            tax_amount = tax_amount + rec.tax_amount
            discount_amount = discount_amount + rec.discount_amount
            pf = pf + rec.pf

        total = sub_total_amount + self.others
        self.grand_amount = round(total)
        self.round_off = round(total) - total
        self.cgst = cgst
        self.sgst = sgst
        self.igst = igst
        self.sub_total_amount = sub_total_amount
        self.tax_amount = tax_amount
        self.un_tax_amount = self.others
        self.pf = pf
        self.discount_amount = discount_amount

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        vals["writter"] = "Quotation created by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        return super(Quotation, self).create(vals)
