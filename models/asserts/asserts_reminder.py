# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class AssertReminder(models.Model):
    _name = "asserts.reminder"
    _inherit = "mail.thread"
    _rec_name = "asserts_id"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    asserts_id = fields.Many2one(comodel_name="arc.asserts", string="Assert")
    person_id = fields.Many2one(comodel_name="arc.person", string="Employee", required=True)
    description = fields.Text(string="Reminder", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.model
    def create(self, vals):
        vals["writter"] = "Assert reminder Created by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        return super(AssertReminder, self).create(vals)
