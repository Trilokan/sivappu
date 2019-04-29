# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime, timedelta

END_INFO = [('current_day', 'Current Day'), ('next_day', 'Next Day')]


# Shift Master
class Shift(models.Model):
    _name = "time.shift"
    _inherit = "mail.thread"

    name = fields.Char(string="Shift", required=True)
    total_hours = fields.Float(string="Total Hours", readonly=True)
    end_day = fields.Selection(selection=END_INFO, string="Ends On", default="current_day")
    from_hours = fields.Integer(string="From Hours", required=True, default=0)
    from_minutes = fields.Integer(string="From Minutes", required=True, default=0)
    till_hours = fields.Integer(string="Till Hours", required=True, default=0)
    till_minutes = fields.Integer(string="Till Minutes", required=True, default=0)
    grace_time = fields.Integer(string="Grace Time (Min)", required=True, default=0)

    _sql_constraints = [("name", "unique(name)", "Shift must be unique")]

    @api.multi
    def trigger_calculate(self):

        today = datetime.strptime("2018-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

        from_date = today + timedelta(hours=self.from_hours) + timedelta(minutes=self.from_minutes)
        till_date = today + timedelta(hours=self.till_hours) + timedelta(minutes=self.till_minutes)

        if self.end_day == 'next_day':
            till_date = till_date + timedelta(days=1)

        secs = (till_date - from_date).seconds

        minutes = ((secs / 60) % 60) / 60.0
        hours = secs / 3600

        self.total_hours = hours + minutes
