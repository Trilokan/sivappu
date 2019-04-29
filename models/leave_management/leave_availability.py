# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("posted", "Posted")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class LeaveAvailability(models.TransientModel):
    _name = "leave.availability"

    person_id = fields.Many2one(comodel_name="arc.person", string="Employee")
    leave_availability = fields.Html(string="Leave Availability", readonly=True)

    @api.onchange("person_id")
    def onchange_person_id(self):
        if self.person_id.id:
            employee_id = self.env["hr.employee"].search([("person_id", "=", self.person_id.id)])
            self.leave_availability = self.get_leave_availability()

    def get_leave_availability(self):
        config = self.env["leave.config"].search([("company_id", "=", self.env.user.company_id.id)])
        template = config.leave_availability_template

        data = ""
        period_id = self.env["arc.period"].get_month(CURRENT_DATE)

        if period_id:
            recs = self.env["leave.details"].search([("work_id.month_id.period_id", "=", period_id.id)])

            for rec in recs:
                data = "{0}<tr><th>{1}</th><th>{2}</th></tr>".format(data, rec.type_id.name, rec.opening)

        return template.format(data)

