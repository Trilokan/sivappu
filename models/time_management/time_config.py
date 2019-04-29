# -*- coding: utf-8 -*-

from odoo import fields, models


# Time Configuration
class TimeConfig(models.Model):
    _name = "time.config"
    _inherit = "mail.thread"
    _rec_name = "company_id"

    half_day = fields.Float(string="Half Day", default=0, required=True)
    full_day = fields.Float(string="Full Day", default=0, required=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id, readonly=True)
