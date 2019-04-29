# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]
PRODUCT_TYPE = [("stockable", "Stockable"), ("others", "Others")]


class Product(models.Model):
    _name = "arc.product"

    image = fields.Binary(string="Image")
    name = fields.Char(string="Name", required=True)
    product_uid = fields.Char(string="Code", readonly=True)
    product_group_id = fields.Many2one(comodel_name="product.group", string="Group", required=True)
    sub_group_id = fields.Many2one(comodel_name="product.sub.group", string="Sub Group", required=True)
    category_id = fields.Many2one(comodel_name="product.category", string="Category", required=True)
    types = fields.Selection(selection=PRODUCT_TYPE, string="Type", required=True, default="stockable")
    uom_id = fields.Many2one(comodel_name="product.uom", string="UOM", required=True)
    hsn_code = fields.Char(string="HSN Code", required=True)
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    description = fields.Text(string="Description")
    warehouse_ids = fields.One2many(comodel_name="store.warehouse",
                                    string="Warehouse",
                                    compute="get_warehouse_ids")

    # Accounting
    payable_id = fields.Many2one(comodel_name="arc.account", string="Payable")
    receivable_id = fields.Many2one(comodel_name="arc.account", string="Receivable")

    # Smart Button
    assert_count = fields.Float(string="Assert", compute="get_assert_count")
    sale_invoice_count = fields.Float(string="Sale Invoice", compute="get_assert_count")
    purchase_invoice_count = fields.Float(string="Purchase Invoice", compute="get_assert_count")
    sale_order_count = fields.Float(string="Sale Order", compute="get_assert_count")
    purchase_order_count = fields.Float(string="Purchase Order", compute="get_assert_count")
    stock_count = fields.Float(string="Available Stock", compute="get_stock_count")
    stock_value = fields.Float(string="Stock Value", compute="get_stock_value")
    incoming_shipment = fields.Float(string="Incoming Shipment", compute="get_assert_count")

    _sql_constraints = [("product_uid", "unique(product_uid)", "Product Code must be unique")]

    # Smart Button
    def action_view_assert(self):
        pass

    def get_assert_count(self):
        return 0

    def get_stock_count(self):
        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])
        for rec in self:
            rec.stock_count = self.env["arc.stock"].get_current_stock(rec.id, config.store_id.id)

        return True

    def get_stock_value(self):
        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])
        for rec in self:
            rec.stock_value = self.env["arc.stock"].get_current_stock_value(rec.id, config.store_id.id)
        return True

    @api.one
    def get_warehouse_ids(self):
        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])
        domain = [('location_id.location_left', '>=', config.store_id.location_left),
                  ('location_id.location_right', '<=', config.store_id.location_right),
                  ('product_id', '=', self.id)]

        self.warehouse_ids = self.env["store.warehouse"].search(domain)

    @api.multi
    def trigger_confirm(self):
        config = self.env["store.config"].search([("company_id", "=", self.env.user.company_id.id)])
        store_location_id = config.store_id.id

        if not store_location_id:
            raise exceptions.ValidationError("Default Product Location is not set")

        # Generate Warehouse of default store location
        self.env["store.warehouse"].create({"product_id": self.id, "location_id": store_location_id})

        # Generate Code on confirmation
        group_uid = self.product_group_id.group_uid
        sub_group_uid = self.sub_group_id.sub_group_uid
        sequence = self.env["ir.sequence"].next_by_code(self._name)

        product_uid = "{0}/{1}/{2}".format(group_uid, sub_group_uid, sequence)

        self.write({"progress": "confirmed", "product_uid": product_uid})

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.product_uid, record.name)
            result.append((record.id, name))
        return result

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

