# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTax(models.Model):
    _name = "product.tax"

    name = fields.Char(string="Name", required=True)
    tax_uid = fields.Char(string="Code", required=True)
    rate = fields.Float(string="Rate", default=0.0, required=True)

    _sql_constraints = [("tax_uid", "unique(tax_uid)", "Tax must be unique"),
                        ("name_rate", "unique(name, rate)", "Tax must be unique")]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "{0}-{1}%".format(record.name, record.rate)
            result.append((record.id, name))
        return result
