# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Bed(models.Model):
    _name = "arc.bed"

    name = fields.Char(string="Name", required=True)
    bed_uid = fields.Char(string="Code", required=True)
    ward_id = fields.Many2one(comodel_name="arc.ward", string="Ward")
