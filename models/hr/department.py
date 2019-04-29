# -*- coding: utf-8 -*-

from odoo import models, fields


# Department
class HRDepartment(models.Model):
    _name = "hr.department"

    name = fields.Char(string="Department", required=True)
    head_id = fields.Many2one(comodel_name="hr.employee", string="Department Head")
    member_ids = fields.Many2many(comodel_name="hr.employee", string="Department Members")
    location_id = fields.Many2one(comodel_name="store.location", string="Stock Location")

    _sql_constraints = [("name", "unique(name)", "Department must be unique")]
