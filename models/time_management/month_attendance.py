# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("open", "Open"), ("closed", "Closed")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class MonthAttendance(models.Model):
    _name = "month.attendance"
    _inherit = "mail.thread"

    period_id = fields.Many2one(comodel_name="arc.period", string="Month", readonly=True)
    month_detail = fields.One2many(comodel_name="daily.attendance", inverse_name="month_id")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_period_id', 'unique (period_id)', 'Error! Month must be unique')]

    def generate_work_sheet(self):
        recs = self.env["arc.person"].search([("is_employee", "=", True), ("active", "=", True)])

        for rec in recs:
            work_sheet_id = self.env["work.sheet"].create({"person_id": rec.id, "month_id": self.id})
            work_sheet_id.update_opening(rec)

    def close_work_sheet(self):
        recs = self.env["work.sheet"].search([("month_id", "=", self.id)])

        for rec in recs:
            rec.update_closing()

    @api.multi
    def trigger_open(self):
        self.generate_work_sheet()
        writter = "Month Open by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "open", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_close(self):
        self.close_work_sheet()
        writter = "Month Closed by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "closed", "writter": writter}

        self.write(data)
