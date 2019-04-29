# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]
CONSUMPTION_INFO = [("before_food", "Before Food"), ("after_food", "After Food")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class Prescription(models.Model):
    _name = "arc.prescription"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", required=True)
    patient_id = fields.Many2one(comodel_name="arc.person", string="Patient", required=True)
    doctor_id = fields.Many2one(comodel_name="arc.person", string="Doctor", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="", default="draft")
    comment = fields.Text(string="Comment")

    total_days = fields.Float(string="Total Days", default=0.0)


class PrescriptionDetail(models.Model):
    _name = "prescription.detail"

    product_id = fields.Many2one(comodel_name="arc.product", string="Medicine", required=True)
    quantity = fields.Float(string="Quantity", default=0.0, required=True)
    morning = fields.Boolean(string="Morning", default=True)
    afternoon = fields.Boolean(string="Afternoon", default=True)
    evening = fields.Boolean(string="Evening", default=True)
    consumption_type = fields.Selection(selection=CONSUMPTION_INFO, string="Consumption", required=True, default="after_food")
    prescription_id = fields.Many2one(comodel_name="arc.prescription", string="Prescription")
