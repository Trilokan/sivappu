# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("admitted", "Admitted"), ("discharged", "Discharged")]
PATIENT_STATUS = [("normal", "Normal"), ("emergency", "Emergency")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class AdDis(models.Model):
    _name = "admission.discharge"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft", string="Progress")

    # Admission
    admission_date = fields.Date(string="Admit On", required=True)
    admission_reason = fields.Many2one(comodel_name="admission.reason", string="Reason", required=True)
    admission_reason_detail = fields.Text(string="Reason Detail")
    admission_contact_person = fields.Char(string="Contact Person")
    admission_contact = fields.Char(string="Contact No")
    admission_by = fields.Char(string="Admit By")
    admission_attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    admission_comment = fields.Text(string="Comment")
    admission_patient_status = fields.Selection(selection=PATIENT_STATUS, default="normal", required=True)
    bed_id = fields.Many2one(comodel_name="arc.bed", required=True)

    # Discharge
    discharge_date = fields.Date(string="Discharge On")
    discharge_reason = fields.Many2one(comodel_name="discharge.reason", string="Reason")
    discharge_reason_detail = fields.Text(string="Reason Detail")
    discharge_contact_person = fields.Char(string="Contact Person")
    discharge_contact = fields.Char(string="Contact No")
    discharge_by = fields.Char(string="Discharge By")
    discharge_attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    discharge_comment = fields.Text(string="Comment")
    discharge_patient_status = fields.Selection(selection=PATIENT_STATUS, default="normal", required=True)
    is_doctor_approved = fields.Boolean(string="Is Doctor Approved")
    is_account_approved = fields.Boolean(string="Is Account Approved")

    admission_writter = fields.Text(string="Writter", track_visibility="always")
    discharge_writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_admit(self):
        writer = "{0} admitted by {1} on {2}".format(self.patient_id.name, self.env.user.name, INDIA_TIME)
        self.write({"progress": "admitted", "admission_writter": writer})

    @api.multi
    def trigger_discharge(self):
        if not self.is_doctor_approved:
            raise exceptions.ValidationError("Error! Doctor approval required before discharge")

        if not self.is_account_approved:
            raise exceptions.ValidationError("Error! Account approval required before discharge")

        writer = "{0} admitted by {1} on {2}".format(self.patient_id.name, self.env.user.name, INDIA_TIME)
        self.write({"progress": "discharged", "discharge_writter": writer})

    @api.multi
    def trigger_doctor_approved(self):
        self.write({"is_doctor_approved": True})

    @api.multi
    def trigger_account_approved(self):
        self.write({"is_doctor_approved": True})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(AdDis, self).create(vals)

