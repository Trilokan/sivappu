# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductCategory(models.Model):
    _name = "product.category"

    name = fields.Char(string="Name", required=True)
    category_uid = fields.Char(string="Code", required=True)
    description = fields.Text(string="Description")

    _sql_constraints = [("code", "unique(category_uid)", "Product Category must be unique")]
