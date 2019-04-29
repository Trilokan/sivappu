# -*- coding: utf-8 -*-

from odoo import models, fields


class StoreLocation(models.Model):
    _name = "store.location"
    _rec_name = "location_uid"

    name = fields.Char(string="Name", required=True)
    location_uid = fields.Char(string="Code", compute="_get_code")
    location_left = fields.Integer(string="Location Left", required=True)
    location_right = fields.Integer(string="Location Right", required=True)

    def _get_code(self):
        for record in self:
            recs = self.env["store.location"].search([("location_left", "<=", record.location_left),
                                                      ("location_right", ">=", record.location_right)])

            recs = recs.sorted(key=lambda r: r.location_left)
            record.location_uid = "/".join(str(x.name) for x in recs)
