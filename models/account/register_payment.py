# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "draft"), ("registered", "Registered")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class RegisterPayment(models.Model):
    _name = "register.payment"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)

    is_payable = fields.Boolean(string="Is Payable")
    is_receivable = fields.Boolean(string="Is Receivable")

    is_amount = fields.Boolean(string="Is Amount")
    is_cr_dr = fields.Boolean(string="Is Cr/Dr note")

    person_id = fields.Many2one(comodel_name="arc.person", string="Person")
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")
    note_id = fields.Many2one(comodel_name="journal.detail", string="Journal Item")
    amount = fields.Float(string="Amount", required=True, default=0.0)

    item_report = fields.Html(string="Item report")
    payment_report = fields.Html(string="Payment report")
    comment = fields.Text(string="Comment")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

