# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

PROGRESS_INFO = [('draft', 'Draft'), ('registered', 'Registered')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class HRComplaint(models.Model):
    _name = "hr.complaint"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Employee",
                                domain="[('is_employee', '=', True)]", required=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", readonly=True)
    designation_id = fields.Many2one(comodel_name="hr.designation", string="Designation", readonly=True)
    complaint_details = fields.Html(string="Complaint Details", required=True)
    action_taken_details = fields.Html(string="Action Taken", required=True)
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    complaints_by = fields.Many2one(comodel_name="arc.person", string="Complaints By", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Char(string="Writter", track_visibility="always")

    @api.multi
    def trigger_register(self):
        writter = "Complaints register by {0} on {1}".format(self.env.user.name, CURRENT_TIME_INDIA)
        self.write({"progress": "registered", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        employee_id = self.env["hr.employee"].search([("person_id", "=", vals["person_id"])])

        vals["department_id"] = employee_id.department_id.id
        vals["designation_id"] = employee_id.designation_id.id

        return super(HRComplaint, self).create(vals)
