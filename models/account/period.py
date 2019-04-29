# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("open", "Open"), ("closed", "Closed")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class ArcPeriod(models.Model):
    _name = "arc.period"
    _inherit = "mail.thread"

    name = fields.Char(string="Period", required=True)
    year_id = fields.Many2one(comodel_name="arc.year", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft", string="Progress")
    is_month = fields.Boolean(string="Is Month", default=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    def get_month(self, date):
        recs = self.env["arc.period"].search([])

        for rec in recs:
            if rec.end_date >= date >= rec.start_date:
                return rec.id

    @api.multi
    def trigger_open(self):
        writter = "Period Open by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "open", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_close(self):
        writter = "Period Closed by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "closed", "writter": writter}

        self.write(data)

    def generate_month_attendance(self, rec_id):
        self.env["month.attendance"].create({"period_id": rec_id.id})

    @api.model
    def create(self, vals):
        rec_id = super(ArcPeriod, self).create(vals)

        if vals.get("is_month", False):
            self.generate_month_attendance(rec_id)

        return rec_id
