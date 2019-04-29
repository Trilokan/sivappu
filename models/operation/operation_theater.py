# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


# Operation Theater
class OperationTheater(models.Model):
    _name = "operation.theater"

    name = fields.Char(string="Name", required=True)
    theater_uid = fields.Char(string="Code", required=True)
    equipment_ids = fields.Many2many(comodel_name="arc.asserts", string="Equipments")
    operation_ids = fields.One2many(comodel_name="patient.operation", inverse_name="ot_id")
    supervisor_id = fields.Many2one(comodel_name="arc.person", string="In-Charge")
    theater_facility = fields.Html(string="Theater Facility")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")