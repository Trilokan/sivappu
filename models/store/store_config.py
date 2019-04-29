# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime


class StoreConfig(models.Model):
    _name = "store.config"
    _inherit = "mail.thread"
    _rec_name = "company_id"

    store_id = fields.Many2one(comodel_name="store.location", string="Store Location")
    purchase_id = fields.Many2one(comodel_name="store.location", string="Purchase Location")
    pharmacy_id = fields.Many2one(comodel_name="store.location", string="Pharmacy Location")
    block_id = fields.Many2one(comodel_name="store.location", string="Block List Location")
    adjustment_id = fields.Many2one(comodel_name="store.location", string="Adjustment Location")
    assert_id = fields.Many2one(comodel_name="store.location", string="Assert Location")
    virtual_left = fields.Integer(string="Virtual Left")
    virtual_right = fields.Integer(string="Virtual Right")
    tax_id = fields.Many2one(comodel_name="product.tax", string="Tax")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)

    def get_material_transact(self, transact_type):
        source_id = destination_id = None

        if transact_type == "in":
            source_id = self.purchase_id.id
            destination_id = self.store_id.id
        elif transact_type == "out":
            source_id = self.store_id.id
            destination_id = self.purchase_id.id

        if not source_id:
            raise exceptions.ValidationError("Error! Source is not configured")

        if not destination_id:
            raise exceptions.ValidationError("Error! Destination is not configured")

        return {"source_id": source_id, "destination_id": destination_id}
    