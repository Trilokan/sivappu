# -*- coding: utf-8 -*-

from odoo import models, fields, api

BLOOD_GROUP = [('a+', 'A+'), ('b+', 'B+'), ('ab+', 'AB+'), ('o+', 'O+'),
               ('a-', 'A-'), ('b-', 'B-'), ('ab-', 'AB-'), ('o-', 'O-')]
GENDER = [('male', 'Male'), ('female', 'Female')]
MARITAL_STATUS = [('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced')]


class Patient(models.Model):
    _name = "arc.patient"

    name = fields.Char(string="Name", required=True)
    patient_uid = fields.Char(string="Patient ID", readonly=True)
    image = fields.Binary(string="Image")
    small_image = fields.Binary(string="Small Image")
    person_id = fields.Many2one(comodel_name="arc.person", string="Person")
    identity_ids = fields.One2many(comodel_name="arc.identity", inverse_name="patient_id")

    # Contact Details
    email = fields.Char(string="e-Mail")
    mobile = fields.Char(string="Mobile")
    phone = fields.Char(string="Phone")

    # Alternate Contact
    alternate_contact_name = fields.Char(string="Name")
    alternate_contact_relation = fields.Char(string="Relation")
    alternate_mobile = fields.Char(string="Mobile")
    alternate_address = fields.Text(string="Address")

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

    # Personnel Details
    age = fields.Integer(string="Age")
    blood_group = fields.Selection(selection=BLOOD_GROUP, string="Blood Group")
    marital_status = fields.Selection(selection=MARITAL_STATUS, string="Marital Status")
    gender = fields.Selection(selection=GENDER, string="Gender")
    caste = fields.Char(string="Caste")
    religion_id = fields.Many2one(comodel_name="arc.religion", string="Religion")
    physically_challenged = fields.Boolean(string="Physically Challenged")
    nationality_id = fields.Many2one(comodel_name="res.country")
    mother_tongue_id = fields.Many2one(comodel_name="arc.language", string="Mother Tongue")
    language_known_ids = fields.Many2many(comodel_name="arc.language", string="Language Known")
    family_member_ids = fields.One2many(comodel_name="arc.address", inverse_name="patient_id")

    # Medical Detail
    allergic_towards = fields.Text(string="Allergic Towards")

    # Attachment
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    def update_person_address(self):
        recs = {}

        recs["name"] = self.name
        recs["person_uid"] = self.patient_uid
        recs["image"] = self.image
        recs["small_image"] = self.small_image

        recs["email"] = self.email
        recs["mobile"] = self.mobile
        recs["phone"] = self.phone

        recs["door_no"] = self.door_no
        recs["building_name"] = self.building_name
        recs["street_1"] = self.street_1
        recs["street_2"] = self.street_2
        recs["locality"] = self.locality
        recs["landmark"] = self.landmark
        recs["city"] = self.city
        recs["state_id"] = self.state_id.id
        recs["country_id"] = self.country_id.id
        recs["pin_code"] = self.pin_code

        recs["is_patient"] = True

        self.person_id.write(recs)

    @api.multi
    def write(self, vals):
        rec = super(Patient, self).write(vals)
        self.update_person_address()
        return rec

    @api.model
    def create(self, vals):
        data = {"person_uid": self.env["ir.sequence"].next_by_code(self._name),
                "is_patient": True,
                "name": vals["name"]}

        data.update(vals)

        person_id = self.env["arc.person"].create(data)
        vals["person_id"] = person_id.id
        vals["patient_uid"] = data["person_uid"]
        return super(Patient, self).create(vals)
