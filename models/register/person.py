# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

PERSON_TYPE = [('doctor', 'Doctor'),
               ('nurse', 'Nurse'),
               ('patient', 'Patient'),
               ('staff', 'Staff'),
               ('teacher', 'Teacher'),
               ('patient', 'Patient'),
               ('student', 'Student'),
               ('supplier', 'Supplier'),
               ('service', 'Service'),
               ('driver', 'Driver')]


class ArcPerson(models.Model):
    _name = "arc.person"

    name = fields.Char(string="Name", required=True)
    person_uid = fields.Char(string="ID Card No", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Small Image")
    active = fields.Boolean(string="Active", default=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 default=lambda self: self.env.user.company_id.id)

    # Professional Details
    email = fields.Char(string="e-Mail")
    mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Phone")
    contact_name = fields.Char(string="Contact Name")
    contact_position = fields.Char(string="Position")

    # Address in Detail
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

    # Account Details
    gst_no = fields.Char(string="GST No")
    license_no = fields.Char(string="License No")
    tin_no = fields.Char(string="TIN No")
    pan_no = fields.Char(string="PAN No")
    driving_license = fields.Char(string="Driving License")
    payable_id = fields.Many2one(comodel_name="arc.account", string="Accounts Payable")
    receivable_id = fields.Many2one(comodel_name="arc.account", string="Accounts Receivable")

    # Filter
    is_employee = fields.Boolean(string="Is Employee")
    is_patient = fields.Boolean(string="Is Patient")
    is_student = fields.Boolean(string="Is Student")
    is_vendor = fields.Boolean(string="Is Vendor")

    person_type = fields.Selection(selection=PERSON_TYPE, string="Person Type")

    def get_account_id(self, invoice_type):
        account_id = False
        if invoice_type in ["sale", "purchase_return"]:
            account_id = self.payable_id.id
        elif invoice_type in ["purchase", "sale_return"]:
            account_id = self.receivable_id.id

        if not account_id:
            msg = "Error! Account is not configured for the {0}".format(self.name)
            raise exceptions.ValidationError(msg)

        return account_id

    def generate_account_id(self, vals):
        data = {"name": vals["name"]}

        payable_id = self.env["arc.account"].create(data)
        receivable_id = self.env["arc.account"].create(data)

        return {"payable_id": payable_id.id, "receivable_id": receivable_id.id}

    @api.model
    def create(self, vals):
        if "person_uid" not in vals:
            vals["person_uid"] = self.env["ir.sequence"].next_by_code(self._name)

        account_data = self.generate_account_id(vals)
        vals.update(account_data)

        return super(ArcPerson, self).create(vals)
