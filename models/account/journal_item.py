# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class JournalDetail(models.Model):
    _name = "journal.detail"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    journal_id = fields.Many2one(comodel_name="arc.journal", string="Journal", required=True)
    period_id = fields.Many2one(comodel_name="arc.period", string="Period")
    entry_id = fields.Many2one(comodel_name="journal.entry", string="Journal Entry")
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")
    description = fields.Text(string="Description")
    person_id = fields.Many2one(comodel_name="arc.person", string="Person")
    account_id = fields.Many2one(comodel_name="arc.account", string="Account")
    credit = fields.Float(string="Credit", default=0.0, required=True)
    debit = fields.Float(string="Debit", default=0.0, required=True)
    ref = fields.Char(string="Reference")
    comment = fields.Text(string="Comment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", related="entry_id.progress")
    writter = fields.Text(string="Writter", track_visibility="always")
