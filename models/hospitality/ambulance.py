# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"),
                 ("confirmed", "Confirmed"),
                 ("driver_intimated", "Driver to Intimated"),
                 ("done", "Done"),
                 ("cancel", "Cancel")]
CANCEL_INFO = [("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Ambulance
class Ambulance(models.Model):
    _name = "arc.ambulance"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    driver_id = fields.Many2one(comodel_name="arc.person", string="Driver", required=True)
    patient_id = fields.Many2one(comodel_name="arc.person", string="Patient", required=True)

    source_address = fields.Text(string="Address")
    source_landmark = fields.Char(string="Landmark")
    source_contact = fields.Char(string="Contact 1")
    source_contact_2 = fields.Char(string="Contact 2")

    destination_address = fields.Text(string="Address")
    destination_landmark = fields.Char(string="Landmark")
    destination_contact = fields.Char(string="Contact 1")
    destination_contact_2 = fields.Char(string="Contact 2")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    is_cancel = fields.Selection(selection=CANCEL_INFO, string="Is Cancel")
    distance = fields.Float(string="Distance(KM)", default=0.0, required=True)
    charges_km = fields.Float(string="Charges (per KM)", default=0.0, required=True)
    others = fields.Float(string="Others", default=0.0, required=True)
    total_amount = fields.Float(string="Total", default=0.0, required=True)

    writter = fields.Text(string="Writter", track_visibility="always")

    @api.multi
    def trigger_confirm(self):
        writter = "Ambulance confirmed by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_inform_driver(self):
        writter = "Ambulance Informed to {0} by {1} on {2}".format(self.driver_id.name, self.env.user.name, INDIA_TIME)
        self.write({"progress": "confirmed", "writter": writter})

    @api.multi
    def trigger_done(self):
        writter = "{0} Shifted {1} by on {2}".format(self.patient_id.name, self.driver_id.name, INDIA_TIME)
        self.write({"progress": "done", "writter": writter})

    @api.multi
    def trigger_cancel(self):
        writter = "Ambulance cancelled by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "confirmed", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(Ambulance, self).create(vals)
