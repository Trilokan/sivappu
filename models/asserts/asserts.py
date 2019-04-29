# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'), ('confirmed', 'Confirmed')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
INDIA_TIME = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Assert
class Assert(models.Model):
    _name = "arc.asserts"
    _inherit = "mail.thread"

    image = fields.Binary(string="Image")
    date = fields.Date(string="Date", default=CURRENT_DATE, required=True)
    name = fields.Char(string="Name", readonly=True)
    capitalise_id = fields.Many2one(comodel_name="asserts.capitalisation", string="Capitalisation", readonly=True)

    # Manufacturing Details
    product_id = fields.Many2one(comodel_name="arc.product", string="Product", required=True)
    manufacturer = fields.Char(string="Manufacturer")
    manufactured_date = fields.Date(string="Date of Manufactured")
    expiry_date = fields.Date(string="Date of Expiry")
    serial_no = fields.Char(string="Serial No")
    model_no = fields.Char(string="Manufacturer")
    warranty_date = fields.Date(string="Warranty Date")

    # Seller Details
    vendor_id = fields.Many2one(comodel_name="arc.person", string="Vendor")
    order_date = fields.Date(string="Order Date")
    # order_id = fields.Many2one(comodel_name="purchase.order", string="Purchase Order")
    purchase_date = fields.Date(string="Date of Purchase")
    # invoice_id = fields.Many2one(comodel_name="purchase.invoice", string="Purchase Invoice")
    # vendor_contact = ""
    # vendor_address = ""

    # Maintenance Details
    maintenance_id = fields.Many2one(comodel_name="arc.person", string="Maintenance")
    # service_contact = ""
    # service_address = ""
    maintenance_details = fields.One2many(comodel_name="asserts.maintenance",
                                          inverse_name="asserts_id",
                                          string="Maintenance Details")
    notification_details = fields.One2many(comodel_name="asserts.reminder",
                                           inverse_name="asserts_id",
                                           string="Notification Details")

    # Accounting Details
    account_id = fields.Many2one(comodel_name="arc.account", string="Account")
    depreciation_percentage = fields.Float(string="Depreciation Percentage")
    responsible_id = fields.Many2one(comodel_name="arc.person", string="Responsible Person")
    is_working = fields.Boolean(string="Is Working")
    is_condem = fields.Boolean(string="Is Condem")
    attachment = fields.Many2many(comodel_name="ir.attachment", string="Attachment")

    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    _sql_constraints = [('unique_name', 'unique (name)', 'Error! Assert must be unique')]

    @api.multi
    def trigger_confirm(self):
        writter = "Asserts capitalisation confirmed by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        self.write({"progress": "confirmed", "writter": writter})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        vals["writter"] = "Assert Created by {0} on {1}".format(self.env.user.name, INDIA_TIME)
        return super(Assert, self).create(vals)
