# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions


# Salary Rule Type
class SalaryRuleCode(models.Model):
    _name = "salary.rule.code"
    _inherit = "mail.thread"

    name = fields.Char(string="Name", required=True)
