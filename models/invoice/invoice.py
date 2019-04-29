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


class Invoice(models.Model):
    _name = "arc.invoice"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Person", required=True)
    address = fields.Text(string="Address")
    invoice_detail = fields.One2many(comodel_name="invoice.detail", inverse_name="invoice_id")
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft")
    invoice_type = fields.Selection(selection=INVOICE_TYPE, string="Invoice Type", required=True)
    order_id = fields.Many2one(comodel_name="arc.order", string="Order")

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

    # Accounting
    journal_items = fields.One2many(comodel_name="journal.detail", inverse_name="invoice_id")
    payment_type = fields.Selection(selection=PAYMENT_TYPE, string="Payment Type", required=True)
    balance = fields.Float(string="Balance", compute="_get_balance")

    @api.multi
    def _get_balance(self):
        for rec in self:
            details = rec.journal_items

            credit = debit = 0
            for detail in details:
                credit = credit + detail.credit
                debit = debit + detail.debit

            if rec.payment_type == "payable":
                rec.balance = credit - debit
            elif rec.payment_type == "receivable":
                rec.balance = debit - credit

    @api.multi
    def trigger_confirm(self):
        self.trigger_update_total()
        writter = "Invoice confirmed by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "confirmed", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_cancel(self):
        self.trigger_update_total()
        writter = "Invoice cancelled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "cancel", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_approve(self):
        self.trigger_update_total()
        self.generate_journal_entry()
        writter = "Invoice approved by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "approved", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_update_total(self):
        recs = self.invoice_detail

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

    @api.multi
    def generate_journal_entry(self):

        data = {"date": self.date,
                "journal_id": self.get_journal_id(),
                "reference": self.name,
                "progress": "posted",
                "journal_detail": self.get_journal_detail()}

        self.env["journal.entry"].create(data)

    @api.multi
    def get_journal_detail(self):
        config = self.env["account.config"].search([("company_id", "=", self.env.user.company_id.id)])
        recs = self.invoice_detail

        data = {"date": self.date,
                "journal_id": self.get_journal_id(),
                "person_id": self.person_id.id}

        line_detail = []
        for rec in recs:
            amount = self.get_credit_debit(rec.after_discount)
            description = "{0} \n {1} \n {2}".format(rec.product_id.product_uid,
                                                     rec.product_id.name,
                                                     rec.product_id.description)
            item = {"account_id": rec.product_id.get_account_id(self.invoice_type),
                    "description": description,
                    "credit": amount["credit"],
                    "debit": amount["debit"]}
            item.update(data)
            line_detail.append((0, 0, item))

        # CGST
        amount = self.get_credit_debit(self.cgst)
        item = {"account_id": config.cgst_id.id,
                "description": "CGST",
                "credit": amount["credit"],
                "debit": amount["debit"]}
        item.update(data)
        line_detail.append((0, 0, item))

        # SGST
        amount = self.get_credit_debit(self.sgst)
        item = {"account_id": config.sgst_id.id,
                "description": "SGST",
                "credit": amount["credit"],
                "debit": amount["debit"]}
        item.update(data)
        line_detail.append((0, 0, item))

        # IGST
        amount = self.get_credit_debit(self.igst)
        item = {"account_id": config.igst_id.id,
                "description": "IGST",
                "credit": amount["credit"],
                "debit": amount["debit"]}
        item.update(data)
        line_detail.append((0, 0, item))

        # Round-Off
        amount = self.get_credit_debit(self.round_off)
        item = {"account_id": config.round_off_id.id,
                "description": "Round-Off",
                "credit": amount["credit"],
                "debit": amount["debit"]}
        item.update(data)
        line_detail.append((0, 0, item))

        # Packing & Forwarding
        amount = self.get_credit_debit(self.pf)
        item = {"account_id": config.pf_id.id,
                "description": "Packing and forwarding",
                "credit": amount["credit"],
                "debit": amount["debit"]}
        item.update(data)
        line_detail.append((0, 0, item))

        # Total
        amount = self.get_credit_debit(self.grand_amount)
        description = "Credit for the {0} {1}".format(self.person_id.person_uid,
                                                      self.person_id.name)
        item = {"account_id": self.person_id.get_account_id(self.invoice_type),
                "description": description,
                "invoice_id": self.id,
                "credit": amount["debit"],
                "debit": amount["credit"]}
        item.update(data)
        line_detail.append((0, 0, item))

        return line_detail

    def get_journal_id(self):
        journal_id = False

        if self.invoice_type == "sale":
            journal_id = self.env["arc.journal"].search([("name", "=", "Sales")])
        elif self.invoice_type == "purchase":
            journal_id = self.env["arc.journal"].search([("name", "=", "Purchase")])
        elif self.invoice_type == "sale_return":
            journal_id = self.env["arc.journal"].search([("name", "=", "Sales Return")])
        elif self.invoice_type == "purchase_return":
            journal_id = self.env["arc.journal"].search([("name", "=", "Purchase Return")])

        if not journal_id:
            raise exceptions.ValidationError("Error! Journal Is not set")

        return journal_id.id

    def get_credit_debit(self, amount):
        credit = debit = 0
        if self.invoice_type in ["sale", "purchase_return"]:
            credit = amount
        elif self.invoice_type in ["purchase", "sale_return"]:
            debit = amount

        return {"credit": credit, "debit": debit}

    @api.model
    def create(self, vals):
        sequence = "{0}.{1}".format(self._name, vals["invoice_type"])
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        vals["writter"] = "Invoice created by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        return super(Invoice, self).create(vals)
