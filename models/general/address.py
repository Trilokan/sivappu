# -*- coding: utf-8 -*-

from odoo import models, fields

RELATION_INFO = [('father', 'Father'),
                 ('mother', 'Mother'),
                 ('wife', 'Wife'),
                 ('brother', 'Brother'),
                 ('sister', 'Sister'),
                 ('uncle', 'Uncle'),
                 ('aunt', 'Aunt'),
                 ('grand_father', 'Grand Father'),
                 ('grand_mother', 'Grand Mother'),
                 ('son', 'Son'),
                 ('daughter', 'Daughter')]


# Address
class Address(models.Model):
    _name = "arc.address"

    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee")
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient")
    name = fields.Char(string="Name")
    relation = fields.Selection(selection=RELATION_INFO, string="Relation")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="E-mail")

    # Address
    door_no = fields.Char(string="Door No")
    building_name = fields.Char(string="Building Name")
    street_1 = fields.Char(string="Street 1")
    street_2 = fields.Char(string="Street 2")
    locality = fields.Char(string="locality")
    landmark = fields.Char(string="landmark")
    city = fields.Char(string="City")
    state_id = fields.Many2one(comodel_name="res.country.state", string="State",
                               default=lambda self: self.env.user.company_id.state_id.id)
    country_id = fields.Many2one(comodel_name="res.country", string="Country")
    pin_code = fields.Char(string="Pincode")

