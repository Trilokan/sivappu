# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StoreWarehouse(models.Model):
    _name = "store.warehouse"

    product_id = fields.Many2one(comodel_name="arc.product", string="Product", readonly=True)
    location_id = fields.Many2one(comodel_name="store.location", string="Location", readonly=True)
    quantity = fields.Float(string="Quantity", compute="_get_stock")

    def _get_stock(self):
        for record in self:
            record.quantity = self.env["arc.stock"].get_current_stock(record.product_id.id, record.location_id.id)

    @api.model
    def create(self, vals):
        record = self.env["store.warehouse"].search_count([("product_id", "=", vals["product_id"]),
                                                           ("location_id", "=", vals["location_id"])])

        if not record:
            return super(StoreWarehouse, self).create(vals)
