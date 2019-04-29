# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class InPatient(models.Model):
    _name = "in.patient"

    date = ""
    name = ""
    patient_id = ""
    symptoms_detail = ""
    symptoms_comment = ""
    diagnosis_detail = ""
    diagnosis_comment = ""
    prescription_detail = ""
    comment = ""
