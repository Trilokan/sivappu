# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

APPOINTMENT_TYPE = [("opt", "OPT"), ("ot", "OT"), ("meeting", "Meeting")]
PROGRESS_INFO = [("cancel", "Cancel")]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Appointment
class ARCAppointment(models.Model):
    _name = "arc.appointment"
    _inherit = "mail.thread"

    date = fields.Datetime(string="Date", default=CURRENT_TIME, required=True)
    name = fields.Char(string="Name", readonly=True)
    person_id = fields.Many2one(comodel_name="arc.person", string="Person",
                                default=lambda self: self.env.user.person_id.id,
                                readonly=True)
    appointment_type = fields.Selection(selection=APPOINTMENT_TYPE, default="opt", required=True)
    appointment_for = fields.Many2one(comodel_name="arc.person", string="Person")
    reason = fields.Many2one(comodel_name="appointment.reason", string="Reason")
    operation_id = fields.Many2one(comodel_name="arc.operation", string="Operation")
    comment = fields.Text(string="Comment")
    is_cancel = fields.Selection(selection=PROGRESS_INFO, string="Is Cancel")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.model
    def create(self, vals):
        sequence = "{0}.{1}".format(self._name, vals["appointment_type"])
        vals["name"] = self.env["ir.sequence"].next_by_code(sequence)
        return super(ARCAppointment, self).create(vals)

    @api.multi
    def trigger_cancel(self):
        writter = "Appointment cancel by {0}".format(self.env.user.name)
        self.write({"is_cancel": "cancel", "writter": writter})
