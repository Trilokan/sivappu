# -*- coding: utf-8 -*-

from odoo import models, fields


class DischargeReason(models.Model):
    _name = "discharge.reason"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
