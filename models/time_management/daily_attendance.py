# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime, timedelta


PROGRESS_INFO = [('draft', 'Draft'), ('verified', 'Verified')]
AVAIL_PROGRESS = [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')]
DAY_PROGRESS = [('holiday', 'Holiday'), ('working_day', 'Working Day')]


# Daily Attendance
class DailyAttendance(models.Model):
    _name = "daily.attendance"
    _rec_name = "date"

    date = fields.Date(string="Date", readonly=True)
    month_id = fields.Many2one(comodel_name="month.attendance", string="Month", readonly=True)
    attendance_detail = fields.One2many(comodel_name="employee.attendance", inverse_name="attendance_id")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', default="draft")
    present = fields.Integer(string="Present", readonly=True)
    half_day_present = fields.Integer(string="Half Day Present", readonly=True)
    absent = fields.Integer(string="Absent", readonly=True)
    employee_count = fields.Integer(string="Employee Count", readonly=True)
    week_off_count = fields.Integer(string="Week-Off Count", readonly=True)
    working_count = fields.Integer(string="Working Count", readonly=True)

    @api.multi
    def trigger_progress(self):
        self.get_availability_progress()
        self.get_report()

    @api.multi
    def trigger_verify(self):
        self.trigger_progress()
        data = {"progress": "verified"}
        self.write(data)

    @api.multi
    def get_report(self):
        rec_obj = self.env["employee.attendance"]
        self.employee_count = rec_obj.search_count([("attendance_id", "=", self.id)])
        self.week_off_count = rec_obj.search_count([("day_progress", "=", "holiday"), ("attendance_id", "=", self.id)])
        self.working_count = rec_obj.search_count([("day_progress", "=", "working_day"), ("attendance_id", "=", self.id)])
        self.present = rec_obj.search_count([("availability_progress", "=", "full_day"), ("attendance_id", "=", self.id)])
        self.half_day_present = rec_obj.search_count([("availability_progress", "=", "half_day"), ("attendance_id", "=", self.id)])
        self.absent = rec_obj.search_count([("availability_progress", "=", "absent"), ("attendance_id", "=", self.id)])

    @api.multi
    def get_availability_progress(self):
        recs = self.attendance_detail

        for rec in recs:
            rec.update_hours()
            rec.trigger_get_availability_progress()

    _sql_constraints = [('unique_attendance',
                         'unique (date)',
                         'Error! Date should not be repeated')]

