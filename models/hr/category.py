# -*- coding: utf-8 -*-

from odoo import models, fields


# Category
class HRCategory(models.Model):
    _name = "hr.category"

    name = fields.Char(string="Category", required=True)

    _sql_constraints = [("name", "unique(name)", "Employee Category must be unique")]
