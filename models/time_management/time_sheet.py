# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime, timedelta

TIME_DELAY_HRS = 5
TIME_DELAY_MIN = 30

PROGRESS_INFO = [('in', 'In'), ('out', 'Out')]
PROCESS_INFO = [('manual', 'Manual'), ('automatic', 'Automatic')]


# Time Sheet
class TimeSheet(models.Model):
    _name = "time.sheet"
    _rec_name = "person_id"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date")
    person_id = fields.Many2one(comodel_name="arc.person", string="Employee")
    progress = fields.Selection(PROGRESS_INFO, string='Progress')
    process = fields.Selection(PROCESS_INFO, string='Process', default="manual", readonly=True)
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.model
    def create(self, vals):
        vals["writter"] = "Time sheet Updated by {0}".format(self.writter)
        current_time = datetime.strptime(vals['date'], "%Y-%m-%d %H:%M:%S")
        time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        config = self.env["time.config"].search([("company_id", "=", self.env.user.company_id.id)])
        accepted_in_time = config.in_time
        accepted_out_time = config.out_time

        recs = self.env["employee.attendance"].search([("person_id", "=", vals["person_id"])])

        for rec in recs:
            expected_from_time = datetime.strptime(rec.expected_from_time, "%Y-%m-%d %H:%M:%S")
            expected_till_time = datetime.strptime(rec.expected_till_time, "%Y-%m-%d %H:%M:%S")

            expected_from_time_grace = expected_from_time - timedelta(minutes=accepted_in_time)
            expected_till_time_grace = expected_till_time + timedelta(minutes=accepted_out_time)

            if 'in' in vals['progress']:
                if expected_from_time_grace <= current_time <= expected_till_time_grace:
                    rec.write({"actual_from_time": time})

            elif 'out' in vals['progress']:
                if expected_from_time_grace <= current_time <= expected_till_time_grace:
                    rec.write({"actual_till_time": time})

        return super(TimeSheet, self).create(vals)
