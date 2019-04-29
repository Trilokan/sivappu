# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta

PROGRESS_INFO = [('draft', 'Draft'), ('open', 'Open'), ("closed", "Closed")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class VacancyPosition(models.Model):
    _name = "vacancy.position"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    designation_id = fields.Many2one(comodel_name="hr.designation", string="Designation")
    contact_id = fields.Many2one(comodel_name="arc.person", string="Contact Person")
    job_description = fields.Html(string="Job Description", required=True)
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

    @api.multi
    def trigger_open(self):
        writter = "Vacancy Opening from {0}".format(CURRENT_TIME_INDIA)
        self.write({"progress": "open", "writter": writter})

    @api.multi
    def trigger_close(self):
        writter = "Vacancy Closed on {0}".format(CURRENT_TIME_INDIA)
        self.write({"progress": "closed", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(VacancyPosition, self).create(vals)

