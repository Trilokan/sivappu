# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductUOM(models.Model):
    _name = "product.uom"
    _rec_name = "uom_uid"

    name = fields.Char(string="Name", required=True)
    uom_uid = fields.Char(string="Code", required=True)
    variance = fields.Float(string="Variance Percentage", default=0.0, required=True)

    _sql_constraints = [("uom_uid", "unique(uom_uid)", "Unit Of Measurement must be unique")]
