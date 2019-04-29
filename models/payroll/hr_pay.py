# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]


# HR Pay
class HRPay(models.Model):
    _name = "hr.pay"
    _inherit = "mail.thread"
    _rec_name = "person_id"

    person_id = fields.Many2one(comodel_name="arc.person", string="Employee", required=True)
    basic = fields.Float(string="Basic", required=True)
    structure_id = fields.Many2one(comodel_name="salary.structure", string="Salary Structure", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility='always')

    _sql_constraints = [('name_uniq', 'unique(person_id)', 'Payscale is already configured'),
                        ('basic_check', 'CHECK(basic > 1)', 'Check BASIC Pay')]

    def trigger_confirm(self):
        writter = "Pay detail for {0} with basic {1} Created by {2}".format(self.person_id.name,
                                                                            self.basic,
                                                                            self.env.user.name)
        self.write({"progress": "confirmed", "writter": writter})

    @api.model
    def create(self, vals):
        person_id = self.env["arc.person"].search([("id", "=", vals["person_id"])])
        writter = "Pay detail for {0} with basic {1} Created by {2}"
        vals["writter"] = writter.format(person_id.name, vals["basic"], self.env.user.name)

        return super(HRPay, self).create(vals)
