# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


# Operation
class Operation(models.Model):
    _name = "arc.operation"

    name = fields.Char(string="Name", readonly=True)
    operation_uid = fields.Char(string="Code", readonly=True)
    procedure = fields.Html(string="Operation Procedure")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    _sql_constraints = [("name", "unique(name)", "Operation must be unique"),
                        ("operation_uid", "unique(operation_uid)", "Operation must be unique")]
