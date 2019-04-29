# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Doctor Timing
class DoctorTiming(models.Model):
    _name = "doctor.timing"

    person_id = fields.Many2one(comodel_name="arc.person", string="Doctor")
    monday_fn_start = fields.Float()
    monday_fn_end = fields.Float()
    monday_an_start = fields.Float()
    monday_an_end = fields.Float()

    tuesday_fn_start = fields.Float()
    tuesday_fn_end = fields.Float()
    tuesday_an_start = fields.Float()
    tuesday_an_end = fields.Float()

    wednesday_fn_start = fields.Float()
    wednesday_fn_end = fields.Float()
    wednesday_an_start = fields.Float()
    wednesday_an_end = fields.Float()

    thursday_fn_start = fields.Float()
    thursday_fn_end = fields.Float()
    thursday_an_start = fields.Float()
    thursday_an_end = fields.Float()

    friday_fn_start = fields.Float()
    friday_fn_end = fields.Float()
    friday_an_start = fields.Float()
    friday_an_end = fields.Float()

    saturday_fn_start = fields.Float()
    saturday_fn_end = fields.Float()
    saturday_an_start = fields.Float()
    saturday_an_end = fields.Float()

    sunday_fn_start = fields.Float()
    sunday_fn_end = fields.Float()
    sunday_an_start = fields.Float()
    sunday_an_end = fields.Float()
