# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class AccountConfig(models.Model):
    _name = "account.config"
    _inherit = "mail.thread"
    _rec_name = "company_id"

    cgst_id = fields.Many2one(comodel_name="arc.account", string="CGST")
    sgst_id = fields.Many2one(comodel_name="arc.account", string="SGST")
    igst_id = fields.Many2one(comodel_name="arc.account", string="IGST")
    round_off_id = fields.Many2one(comodel_name="arc.account", string="Round Off")
    pf_id = fields.Many2one(comodel_name="arc.account", string="Packing Forwarding")

    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id,
                                 readonly=True)
