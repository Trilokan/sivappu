# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'),
                 ('confirmed', 'Waiting For Approval'),
                 ('cancelled', 'Cancelled'),
                 ('approved', 'Approved')]
TOTAL_DAYS = [("half_day", "Half Day"), ("full_day", "Full Day")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class CompOffApplication(models.Model):
    _name = "comp.off.application"

    date = fields.Date(string="From Date", default=CURRENT_DATE, required=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Person", required=True)
    reason = fields.Text(string="Reason")
    total_days = fields.Selection(selection=TOTAL_DAYS, string="Total Days", default="full_day", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def check_month(self):
        attendance_id = self.env["employee.attendance"].search([("attendance_id.date", "=", self.date),
                                                                ("person_id", "=", self.person_id.id)])

        if not attendance_id:
            raise exceptions.ValidationError("Error! Month is not configured")

        if attendance_id.attendance_id.month_id.progress == "closed":
            raise exceptions.ValidationError("Error! Month is already closed")

    @api.multi
    def trigger_confirm(self):
        self.check_month()
        writter = "Comp-Off application confirmed by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "confirmed", "writter": writter}

        self.write(data)

    @api.multi
    def trigger_cancel(self):
        self.check_month()
        writter = "Comp-Off application cancelled by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "cancelled", "writter": writter}

        self.write(data)

    def update_work_sheet(self):
        config = self.env["leave.config"].search([("company_id", "=", self.env.user.company_id.id)])

        leave_details_id = self.env["leave.details"].search([("work_id.person_id", "=", self.person_id.id),
                                                             ("work_id.month_id.period_id.start_date", ">=", self.date),
                                                             ("work_id.month_id.period_id.end_date", "<=", self.date),
                                                             ("work_id.type_id", "=", config.co_id.id)])

        if self.total_days == "half_day":
            leave_details_id.credit = leave_details_id.credit + 0.5
        elif self.total_days == "full_day":
            leave_details_id.credit = leave_details_id.credit + 1

    @api.multi
    def trigger_approve(self):
        self.check_month()
        self.update_work_sheet()
        writter = "Comp-Off application approved by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        data = {"progress": "approved", "writter": writter}

        self.write(data)

    @api.model
    def create(self, vals):
        vals["writter"] = "Comp-Off application created by {0}".format(self.env.user.name)
        return super(CompOffApplication, self).create(vals)
