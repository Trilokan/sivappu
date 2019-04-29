# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "draft"), ("registered", "Registered")]
PAYMENT_TYPE = [("payable", "Payable"), ("receivable", "Receivable")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class RegisterPayment(models.Model):
    _name = "register.payment"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)

    payment_type = fields.Selection(selection=PAYMENT_TYPE, string="Payment Type")

    is_amount = fields.Boolean(string="Is Amount")
    is_cdr = fields.Boolean(string="Is Cr/Dr note")

    person_id = fields.Many2one(comodel_name="arc.person", string="Person")
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")
    note_id = fields.Many2one(comodel_name="journal.detail", string="Journal Item")
    amount = fields.Float(string="Amount", required=True, default=0.0)

    item_report = fields.Html(string="Item report")
    payment_report = fields.Html(string="Payment report")
    comment = fields.Text(string="Comment")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

    def split_journal_item(self):
        pass

    def reconcile_journal(self):
        pass

    def reconcile_payment(self):
        balance = self.invoice_id.balance

        if self.amount > balance:
            raise exceptions.ValidationError("Error! Payment amount is greater than Invoice amount")

        self.generate_journal_entry(self.invoice_id.id)

    @api.multi
    def trigger_register_payment(self):

        if self.is_amount:
            if self.invoice_id:
                self.reconcile_payment()
            else:
                self.generate_journal_entry()
        elif self.is_cdr:
            if self.invoice_id:
                self.reconcile_journal()
            else:
                raise exceptions.ValidationError("Error! ")

    @api.multi
    def get_account_id(self):
        account_id = False
        if self.payment_type == "payable":
            account_id = self.person_id.payable_id.id
        elif self.payment_type == "receivable":
            account_id = self.person_id.receivable_id.id

        if not account_id:
            raise exceptions.ValidationError("Error!")

        return account_id

    @api.multi
    def generate_journal_entry(self, invoice_id=False):

        data = {"date": self.date,
                "journal_id": self.get_journal_id(),
                "reference": self.name,
                "progress": "posted",
                "journal_detail": self.get_journal_detail(invoice_id)}

        print data
        self.env["journal.entry"].create(data)

    @api.multi
    def get_journal_detail(self, invoice_id=False):
        config = self.env["account.config"].search([("company_id", "=", self.env.user.company_id.id)])

        data = {"date": self.date,
                "journal_id": self.get_journal_id(),
                "person_id": self.person_id.id}

        line_detail = []

        # Bank Pay
        amount = self.get_credit_debit("Bank", self.amount)
        item = {"account_id": config.bank_id.id,
                "description": "Bank Payment",
                "credit": amount["credit"],
                "debit": amount["debit"]}
        item.update(data)
        line_detail.append((0, 0, item))

        # Cr/Dr
        amount = self.get_credit_debit("Person", self.amount)
        item = {"account_id": self.get_account_id(),
                "description": "Person Payment",
                "invoice_id": invoice_id,
                "credit": amount["credit"],
                "debit": amount["debit"]}
        item.update(data)
        line_detail.append((0, 0, item))

        return line_detail

    def get_journal_id(self):
        journal_id = False

        if self.payment_type == "payable":
            journal_id = self.env["arc.journal"].search([("name", "=", "Payable")])
        elif self.payment_type == "receivable":
            journal_id = self.env["arc.journal"].search([("name", "=", "Receivable")])

        if not journal_id:
            raise exceptions.ValidationError("Error! Journal Is not set")

        return journal_id.id

    def get_credit_debit(self, payment, amount):
        if (self.payment_type == "payable") and (payment == "Bank"):
            return {"credit": amount, "debit": 0}
        elif (self.payment_type == "payable") and (payment == "Person"):
            return {"credit": 0, "debit": amount}
        elif (self.payment_type == "receivable") and (payment == "Bank"):
            return {"credit": 0, "debit": amount}
        elif (self.payment_type == "receivable") and (payment == "Person"):
            return {"credit": amount, "debit": 0}


