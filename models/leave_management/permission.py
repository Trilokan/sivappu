# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Waiting For Approval'),
                 ('cancelled', 'Cancelled'),
                 ('approved', 'Approved')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class PermissionApplication(models.Model):
    _name = "permission.application"

    date = fields.Date(string="Date", default=CURRENT_TIME, required=True)
    from_time = fields.Float(string="From Time", default=0.0, required=True)
    till_time = fields.Float(string="Till Time", default=0.0, required=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Person", required=True)
    reason = fields.Text(string="Reason")
    total_hours = fields.Float(string="Total Hours", default=0.0, required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def check_month(self):
        attendance_id = self.env["employee.attendance"].search([("attendance_id.date", "=", self.date),
                                                                ("person_id", "=", self.person_id.id)])

        if not attendance_id:
            raise exceptions.ValidationError("Error! Month is not configured")

        if attendance_id.attendance_id.month_id.progress == "closed":
            raise exceptions.ValidationError("Error! Month is already closed")

    def get_min_sec(self, d1, date_obj):
        time_str = str(d1)
        v1, v2 = time_str.split(".")
        v1 = int(v1)
        v2 = (int(v2) * 60) / 100

        res = date_obj + timedelta(hours=v1, minutes=v2)
        return res

    def update_total_hours(self):
        date_obj = datetime.strptime(self.date, "%Y-%m-%d")
        from_time_obj = self.get_min_sec(self.from_time, date_obj)
        till_time_obj = self.get_min_sec(self.till_time, date_obj)

        secs = (till_time_obj - from_time_obj).seconds
        minutes = ((secs / 60) % 60) / 60.0
        hours = secs / 3600

        return hours + minutes

    @api.multi
    def trigger_confirm(self):
        self.check_month()
        writter = "Permission confirmed by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "confirmed",
                "total_hours": self.update_total_hours(),
                "writter": writter}

        self.write(data)

    @api.multi
    def trigger_cancel(self):
        self.check_month()
        writter = "Permission cancelled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "cancelled", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_approve(self):
        self.check_month()
        attendance_id = self.env["employee.attendance"].search([("attendance_id.date", "=", self.date),
                                                                ("person_id", "=", self.person_id.id)])
        attendance_id.permission_hours = self.total_hours

        writter = "Permission approved by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "approved", "writter": writter}

        self.write(data)

    @api.model
    def create(self, vals):
        vals["writter"] = "Permission created by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        return super(PermissionApplication, self).create(vals)
