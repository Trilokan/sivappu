# -*- coding: utf-8 -*-

from odoo import models, fields


# Language
class Language(models.Model):
    _name = "arc.language"

    name = fields.Char(string="Language", required=True)

    _sql_constraints = [("name", "unique(name)", "Language must be unique")]
