# -*- coding: utf-8 -*-

from odoo import models, fields


# Leave Type
class LeaveType(models.Model):
    _name = "leave.type"

    name = fields.Char(string="Name", required=True)
    type_uid = fields.Char(string="Code", required=True)

    _sql_constraints = [("type_uid", "unique(type_uid)", "Leave Type must be unique")]
