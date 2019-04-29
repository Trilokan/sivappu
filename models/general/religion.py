# -*- coding: utf-8 -*-

from odoo import models, fields


# Religion
class Religion(models.Model):
    _name = "arc.religion"

    name = fields.Char(string="Religion", required=True)

    _sql_constraints = [("name", "unique(name)", "Religion must be unique")]
