# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]
MARITAL_INFO = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]
GENDER_INFO = [('male', 'Male'), ('female', 'Female')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class AppointmentOrder(models.Model):
    _name = "appointment.order"
    _inherit = "mail.thread"

    # Resume Details
    date = fields.Date(string="Date", required=True, default=CURRENT_DATE)
    name = fields.Char(string="Name", readonly=True)
    image = fields.Binary(string="Image", related="resume_id.image")
    resume_id = fields.Many2one(comodel_name="resume.bank", string="Resume", required=True)
    candidate_uid = fields.Char(string="Candidate ID", related="resume_id.candidate_uid")

    # Contact Detail
    email = fields.Char(string="Email", related="resume_id.email")
    mobile = fields.Char(string="Mobile", related="resume_id.mobile")

    # Order Detail
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    position_id = fields.Many2one(comodel_name="hr.designation", string="Position", required=True)
    order_preview = fields.Html(string="Order Preview", readonly=1)
    appointment_order = fields.Binary(string="Appointment Order", readonly=1)

    # Salary Details
    salary_detail = fields.One2many(comodel_name="appointment.order.salary",
                                    inverse_name="appointment_id",
                                    string="Salary Detail")

    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility='always')

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].sudo().next_by_code(self._name)
        return super(AppointmentOrder, self).create(vals)


class AppointmentOrderSalary(models.Model):
    _name = "appointment.order.salary"

    name = fields.Char(string="Name")
    amount = fields.Float(string="Amount")
    appointment_id = fields.Many2one(comodel_name="appointment.order", string="Appointment Order")

