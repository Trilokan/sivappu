# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class JournalEntry(models.Model):
    _name = "journal.entry"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    journal_id = fields.Many2one(comodel_name="arc.journal", string="Journal", required=True)
    period_id = fields.Many2one(comodel_name="arc.period", string="Period")
    ref = fields.Char(string="Reference")
    journal_detail = fields.One2many(comodel_name="journal.detail", inverse_name="entry_id")
    comment = fields.Text(string="Comment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_post(self):
        writter = "Journal Entry posted by {0} on {1}".format(self.env.user.name, CURRENT_DATE)
        self.write({"progress": "posted", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(JournalEntry, self).create(vals)
