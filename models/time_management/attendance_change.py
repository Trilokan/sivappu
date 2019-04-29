# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions
from datetime import datetime, timedelta

TIME_DELAY_HRS = -5
TIME_DELAY_MIN = -30

PROGRESS_INFO = [('draft', 'Draft'), ('changed', 'Changed')]
DAY_PROGRESS = [('holiday', 'Holiday'), ('working_day', 'Working Day')]
CHANGE_TYPE = [("holiday_change", "Holiday Change"),
               ("shift_change", "Shift Change"),
               ("add_employee", "Add Employee")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Attendance Change
class AttendanceChange(models.Model):
    _name = "attendance.change"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    reason = fields.Text(string="Reason", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    change_type = fields.Selection(selection=CHANGE_TYPE, string="Change Type")
    person_id = fields.Many2one(comodel_name="arc.person", string="Employee", required=True)
    shift_id = fields.Many2one(comodel_name="time.shift", string="Shift")
    day_progress = fields.Selection(DAY_PROGRESS, string="Day Status")

    def employee_check(self):
        attendance = self.env["employee.attendance"].search([("person_id", "=", self.person_id.id),
                                                             ("attendance_id.date", "=", self.date)])

        if attendance:
            return attendance
        else:
            raise exceptions.ValidationError("Error! Employee Not Available please check")

    def date_check(self):
        date_rec = self.env["daily.attendance"].search([("date", "=", self.date)])

        if not date_rec:
            raise exceptions.ValidationError("Attendance Sheet is not yet generated")

        if date_rec.month_id.progress == "closed":
            raise exceptions.ValidationError("Error! Month is already closed")

    @api.multi
    def trigger_holiday_change(self):
        self.date_check()
        attendance = self.employee_check()
        attendance.write({"day_progress": self.day_progress})
        self.write({"progress": "changed"})

    @api.multi
    def trigger_shift_change(self):
        self.date_check()
        attendance = self.employee_check()
        current_date_obj = datetime.strptime(self.date, "%Y-%m-%d")

        timings = self.env["model.date"].get_expected_time(current_date_obj,
                                                           self.shift_id.from_hours + TIME_DELAY_HRS,
                                                           self.shift_id.from_minutes + TIME_DELAY_MIN,
                                                           self.shift_id.total_hours)

        attendance.write({"shift_id": self.shift_id.id,
                          "expected_from_time": timings["from_time"],
                          "expected_till_time": timings["till_time"]})

        self.write({"progress": "changed"})

    @api.multi
    def trigger_add_employee(self):
        self.date_check()
        self.check_duplicate()

        attendance = self.env["daily.attendance"].search([("date", "=", self.date)])
        current_date_obj = datetime.strptime(self.date, "%Y-%m-%d")

        timings = self.env["model.date"].get_expected_time(current_date_obj,
                                                           self.shift_id.from_hours + TIME_DELAY_HRS,
                                                           self.shift_id.from_minutes + TIME_DELAY_MIN,
                                                           self.shift_id.total_hours)

        data = {"person_id": self.person_id.id,
                "day_progress": "working_day",
                "shift_id": self.shift_id.id,
                "attendance_id": attendance.id,
                "expected_from_time": timings["from_time"],
                "expected_till_time": timings["till_time"]}

        self.env["employee.attendance"].create(data)

    def check_duplicate(self):
        attendance = self.env["daily.attendance"].search([("date", "=", self.date)])
        attendance_detail = self.env["employee.attendance"].search([("person_id", "=", self.person_id.id),
                                                                    ("attendance_id", "=", attendance.id)])

        if attendance_detail:
            raise exceptions.ValidationError("Error! please check employee is already in shift")
