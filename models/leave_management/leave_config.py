# -*- coding: utf-8 -*-

from odoo import models, fields


# Leave Configuration
class LeaveConfig(models.Model):
    _name = "leave.config"
    _rec_name = "company_id"

    lop_id = fields.Many2one(comodel_name="leave.type", string="Loss Of Pay")
    co_id = fields.Many2one(comodel_name="leave.type", string="Comp-Off")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    leave_availability_template = fields.Html(string="Leave Availability Template")