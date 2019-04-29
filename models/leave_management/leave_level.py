# -*- coding: utf-8 -*-

from odoo import models, fields


class LeaveLevel(models.Model):
    _name = "leave.level"

    name = fields.Char(string="Name", required=True)
    level_uid = fields.Char(string="Code", required=True)
    item_ids = fields.One2many(comodel_name="leave.level.item", inverse_name="level_id")

    _sql_constraints = [("level_uid", "unique(level_uid)", "Leave Level must be unique")]


class LeaveLevelItem(models.Model):
    _name = "leave.level.item"
    _order = "sequence"

    sequence = fields.Integer(string="Sequence")
    type_id = fields.Many2one(comodel_name="leave.type", string="Leave Type", required=True)
    credit = fields.Float(string="Leave Credit", default=0.0, required=True)
    level_id = fields.Many2one(comodel_name="leave.level", string="Leave Level", required=True)
