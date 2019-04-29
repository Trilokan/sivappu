# -*- coding: utf-8 -*-

from odoo import models, fields


class AdmissionReason(models.Model):
    _name = "admission.reason"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
