# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


class Reminder(models.Model):
    _name = "arc.reminder"
    _rec_name = "person_id"

    date = fields.Datetime(string="Date", default=CURRENT_TIME, required=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Staff",
                                default=lambda self: self.env.user.person_id.id,
                                required=True)
    reminder = fields.Text(string="Notes", required=True)

