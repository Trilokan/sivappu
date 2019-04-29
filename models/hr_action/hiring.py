# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

PROGRESS_INFO = [('draft', 'Draft'), ('hired', 'Hired')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class HRHiring(models.Model):
    _name = "hr.hiring"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    image = fields.Binary(string="Image")
    employee_name = fields.Char(string="Employee Name", required=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    designation_id = fields.Many2one(comodel_name="hr.designation", string="Designation", required=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", readonly=True)
    category_id = fields.Many2one(comodel_name="hr.category", string="Employee Category", required=True)
    job_description = fields.Html(string="Job Description", required=True)
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    hired_by = fields.Many2one(comodel_name="arc.person", string="Hired By", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    def generate_employee(self):
        employee = {"doj": self.date,
                    "category_id": self.category_id.id,
                    "name": self.employee_name,
                    "image": self.image}

        employee_id = self.env["hr.employee"].create(employee)

        return employee_id

    @api.multi
    def trigger_hire(self):
        employee_id = self.generate_employee()
        writter = "{0} Hiring register by {1}".format(self.employee_name, self.env.user.name)
        self.write({"progress": "hired", "writter": writter, "employee_id": employee_id.id})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(HRHiring, self).create(vals)
