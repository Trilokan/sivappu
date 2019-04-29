# -*- coding: utf-8 -*-

from odoo import models, fields


class Year(models.Model):
    _name = "arc.year"

    name = fields.Char(string="Name", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    