# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"),
                 ("account_approved", "Account Approved"),
                 ("procedure_completed", "Procedure Completed"),
                 ("ot_booked", "OT Booked"),
                 ("done", "Done"),
                 ("cancel", "Cancel")]
CANCEL_INFO = [("cancel", "Cancel")]
PAYMENT_INFO = [("un_paid", "Un-Paid"), ("partially_paid", "Partially Paid"), ("paid", "Paid")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Patient Operation
class PatientOperation(models.Model):
    _name = "patient.operation"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="arc.person", string="Patient", required=True)
    doctor_id = fields.Many2one(comodel_name="arc.person", string="Doctor", required=True)
    staff_ids = fields.Many2many(comodel_name="arc.person", string="Staffs")
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft", string="Progress")

    # Operation
    operation_date = fields.Date(string="Date of Operation", default=CURRENT_DATE, required=True)
    operation_id = fields.Many2one(comodel_name="arc.operation", string="Operation", required=True)
    procedure_ids = fields.Many2many(comodel_name="ir.attachment", string="Procedure", required=True)
    ot_id = fields.Many2one(comodel_name="operation.theater", string="Operation Theater", required=True)
    comment = fields.Text(string="Comment")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    payment = fields.Selection(selection=PAYMENT_INFO, default="un_paid", string="Payment")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_account_approved(self):
        writter = "Accounts Approved by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "account_approved", "writter": writter})

    @api.multi
    def trigger_procedure_completed(self):
        writter = "Operation Procedure Completed by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "procedure_completed", "writter": writter})

    @api.multi
    def trigger_ot_booked(self):
        writter = "Operation Theater Booked by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "ot_booked", "writter": writter})

    @api.multi
    def trigger_done(self):
        writter = "Operation done on {0}".format(INDIA_TIME)
        self.write({"progress": "ot_booked", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Operation Cancel on {0}".format(INDIA_TIME)
        self.write({"progress": "ot_booked", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(PatientOperation, self).create(vals)
