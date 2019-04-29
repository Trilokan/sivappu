# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# Work Sheet
class WorkSheet(models.Model):
    _name = "work.sheet"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Employee", readonly=True)
    month_id = fields.Many2one(comodel_name="month.attendance", string="Month", required=True)
    month_days = fields.Float(string="Days in Month", default=0.0, required=True)
    un_schedule_days = fields.Float(string="Un Schedule Days", default=0.0, required=True)
    schedule_days = fields.Float(string="Schedule Days", default=0.0, required=True)
    working_days = fields.Float(string="Working Days", default=0.0, required=True)
    holidays = fields.Float(string="Holidays", default=0.0, required=True)
    working_days_present = fields.Float(string="Working Days Present", default=0.0, required=True)
    holidays_present = fields.Float(string="Holidays Present Days", default=0.0, required=True)
    ot_days = fields.Float(string="OT Days", default=0.0, required=True)
    co_days = fields.Float(string="Comp-off Days", default=0.0, required=True)
    lop_days = fields.Float(string="Lop Days", default=0.0, required=True)
    leave_taken = fields.Float(string="Leave Taken", default=0.0, required=True)
    leave_details = fields.One2many(comodel_name="leave.details", inverse_name="work_id")
    payslip_id = fields.Many2one(comodel_name="pay.slip", string="Payslip")

    def get_opening(self, person_id):
        start_date = self.month_id.period_id.start_date
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        actual_start_obj = start_date_obj - relativedelta(months=1)
        actual_end_obj = start_date_obj - timedelta(days=1)
        start = actual_start_obj.strftime("%Y-%m-%d")
        end = actual_end_obj.strftime("%Y-%m-%d")

        month_id = self.env["month.attendance"].search([("period_id.start_date", "=", start),
                                                        ("period_id.end_date", "=", end)])

        work_id = self.env["work.sheet"].search([("month_id", "=", month_id.id), ("person_id", "=", person_id.id)])
        recs = work_id.leave_details

        data = {}
        for rec in recs:
            data[rec.name] = rec.closing

        return data

    def get_leave_credit(self, employee_id):
        data = {}
        return data

    @api.multi
    def update_opening(self, person_id):
        employee_id = self.env["hr.employee"].search([("person_id", "=", person_id.id)])

        last_period = self.get_opening(person_id)
        leave_credit = self.get_leave_credit(employee_id)
        recs = employee_id.leave_level_id.item_ids

        for rec in recs:
            leave_type = rec.type_id.name
            data = {"type_id": rec.type_id.id,
                    "level_id": rec.level_id.id,
                    "sequence": rec.sequence,
                    "work_id": self.id,
                    "opening": last_period.get(leave_type, 0),
                    "leave_credit": leave_credit.get(leave_type, 0)}

            self.env["leave.details"].create(data)

    def check_month(self):
        if self.month_id.progress == "closed":
            raise exceptions.ValidationError("Error! Month is already closed")

    def clear_content(self):
        recs = self.leave_details

        for rec in recs:
            rec.reconcile = 0
            rec.closing = 0

    def update_closing(self):
        self.check_month()
        self.clear_content()

        config = self.env["leave.config"].search([("company_id", "=", self.env.user.company_id.id)])
        recs = self.env["leave.details"].search([("type_id", "!=", config.lop_id.id), ("work_id", "=", self.id)])

        leave_taken = self.leave_taken
        for rec in recs:
            total = (rec.opening + rec.credit) - rec.reconcile
            if leave_taken and total:
                if total >= leave_taken:
                    rec.reconcile = rec.reconcile + leave_taken
                    leave_taken = 0
                else:
                    rec.reconcile = rec.reconcile + total
                    leave_taken = leave_taken - total

            rec.closing = (rec.opening + rec.credit) - rec.reconcile
        self.lop_days = leave_taken
