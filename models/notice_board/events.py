# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancel", "Cancel")]
CANCEL_INFO = [("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class ArcEvents(models.Model):
    _name = "arc.event"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", required=True)
    name = fields.Char(string="Name", readonly=True)
    event = fields.Char(string="Event", required=True)
    event_detail = fields.Html(string="Event Detail")
    supervisor_id = fields.Many2one(comodel_name="arc.person", string="Event In-Charge")
    venue = fields.Char(string="Venue")
    timings = fields.Text(string="Timings")
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft")
    is_cancel = fields.Selection(selection=CANCEL_INFO, string="Is Cancel")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        writter = "Events confirm by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Events cancel by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        self.write({"progress": "cancel", "is_cancel": "cancel", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(ArcEvents, self).create(vals)
