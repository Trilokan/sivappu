# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

APPOINTMENT_TYPE = [("opt", "OPT"), ("ot", "OT"), ("meeting", "Meeting")]


# Appointment
class AppointmentReason(models.Model):
    _name = "appointment.reason"

    name = fields.Char(string="Reason", required=True)
    appointment_type = fields.Selection(selection=APPOINTMENT_TYPE, string="Appointment Type", required=True)
