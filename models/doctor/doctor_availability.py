# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class DoctorAvailability(models.Model):
    _name = "doctor.availability"
    _rec_name = "person_id"

    from_date = fields.Date(string="From Date", default=CURRENT_DATE, required=True)
    till_date = fields.Date(string="Till Date", default=CURRENT_DATE, required=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Doctor", required=True)

