# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime, timedelta


PROGRESS_INFO = [('draft', 'Draft'), ('verified', 'Verified')]
AVAIL_PROGRESS = [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')]
DAY_PROGRESS = [('holiday', 'Holiday'), ('working_day', 'Working Day')]


# Employee Attendance
class EmployeeAttendance(models.Model):
    _name = "employee.attendance"

    shift_id = fields.Many2one(comodel_name="time.shift", string="Shift", readonly=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Employee", readonly=True)
    attendance_id = fields.Many2one(comodel_name="daily.attendance", string="Attendance", readonly=True)
    expected_from_time = fields.Datetime(string="Expected From Time", readonly=True)
    actual_from_time = fields.Datetime(string="Actual From Time", readonly=True)
    expected_till_time = fields.Datetime(string="Expected Till Time", readonly=True)
    actual_till_time = fields.Datetime(string="Actual Till Time", readonly=True)
    expected_hours = fields.Float(string="Expected Hours", default=0, readonly=True)
    actual_hours = fields.Float(string="Actual Hours", default=0, readonly=True)
    permission_hours = fields.Float(string="Permission Hours", default=0, readonly=True)
    on_duty_hours = fields.Float(string="On Duty Hours", default=0, readonly=True)
    day_progress = fields.Selection(DAY_PROGRESS, string='Day Status', readonly=True)
    availability_progress = fields.Selection(AVAIL_PROGRESS, string='Availability Status')
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='attendance_id.progress')

    @api.multi
    def update_hours(self):
        if self.expected_from_time and self.expected_till_time:
            expected_from_time = datetime.strptime(self.expected_from_time, "%Y-%m-%d %H:%M:%S")
            expected_till_time = datetime.strptime(self.expected_till_time, "%Y-%m-%d %H:%M:%S")
            self.expected_hours = (expected_till_time - expected_from_time).total_seconds()/(60 * 60)

        if self.actual_from_time and self.actual_till_time:
            actual_from_time = datetime.strptime(self.actual_from_time, "%Y-%m-%d %H:%M:%S")
            actual_till_time = datetime.strptime(self.actual_till_time, "%Y-%m-%d %H:%M:%S")
            self.actual_hours = (actual_till_time - actual_from_time).total_seconds() / (60 * 60)

    @api.multi
    def trigger_get_availability_progress(self):
        config = self.env["time.config"].search([("company_id", "=", self.env.user.company_id.id)])
        full_day = config.full_day
        half_day = config.half_day
        total_hours = self.actual_hours + self.permission_hours + self.on_duty_hours

        if total_hours >= full_day:
            self.availability_progress = "full_day"
        elif total_hours >= half_day:
            self.availability_progress = "half_day"
        else:
            self.availability_progress = "absent"

    _sql_constraints = [('unique_attendance_detail',
                         'unique (attendance_id, person_id)',
                         'Error! Employee should not repeated')]
