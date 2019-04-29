# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("shifted", "Shifted")]
SHIFT_TYPE = [("admission", "Admission"), ("internal", "Internal"), ("discharge", "Discharge")]


class PatientShifting(models.Model):
    _name = "patient.shifting"

    date = ""
    name = ""
    person_id = ""
    source_id = ""
    destination_id = ""
    progress = ""
    shift_type = ""
