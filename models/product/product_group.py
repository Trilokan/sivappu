# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductGroup(models.Model):
    _name = "product.group"

    name = fields.Char(string="Name", required=True)
    group_uid = fields.Char(string="Code", required=True)
    sub_group_ids = fields.One2many(comodel_name="product.sub.group", inverse_name="product_group_id")

    _sql_constraints = [("group_uid", "unique(group_uid)", "Product Group Code must be unique")]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.group_uid, record.name)
            result.append((record.id, name))
        return result
