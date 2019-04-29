# -*- coding: utf-8 -*-

from odoo import models


# Stock
class ArcStock(models.Model):
    _name = "arc.stock"

    def get_stock(self, search_source, search_destination):
        source_ids = self.env["arc.move"].search(search_source)
        destination_ids = self.env["arc.move"].search(search_destination)

        quantity_in = sum(source_ids.mapped("quantity"))
        quantity_out = sum(destination_ids.mapped("quantity"))

        return quantity_in - quantity_out

    def get_current_stock(self, product_id, location_id):
        source_ids = self.env["arc.move"].search([("product_id", "=", product_id),
                                                  ("source_id", "=", location_id),
                                                  ("progress", "=", "moved")])

        destination_ids = self.env["arc.move"].search([("product_id", "=", product_id),
                                                       ("destination_id", "=", location_id),
                                                       ("progress", "=", "moved")])

        quantity_in = sum(source_ids.mapped("quantity"))
        quantity_out = sum(destination_ids.mapped("quantity"))

        return quantity_out - quantity_in

    def get_current_stock_date(self, product_id, location_id, date):
        source_ids = self.env["arc.move"].search([("date", "<=", date),
                                                  ("product_id", "=", product_id),
                                                  ("source_id", "=", location_id),
                                                  ("progress", "=", "moved")])

        destination_ids = self.env["arc.move"].search([("date", "<=", date),
                                                       ("product_id", "=", product_id),
                                                       ("destination_id", "=", location_id),
                                                       ("progress", "=", "moved")])

        quantity_in = sum(source_ids.mapped("quantity"))
        quantity_out = sum(destination_ids.mapped("quantity"))

        return quantity_out - quantity_in

    def get_current_stock_value(self, product_id, location_id):
        source_ids = self.env["arc.move"].search([("product_id", "=", product_id),
                                                  ("source_id", "=", location_id),
                                                  ("progress", "=", "moved")])

        destination_ids = self.env["arc.move"].search([("product_id", "=", product_id),
                                                       ("destination_id", "=", location_id),
                                                       ("progress", "=", "moved")])

        quantity_in = sum(source_ids.mapped("stock_value"))
        quantity_out = sum(destination_ids.mapped("stock_value"))

        return quantity_out - quantity_in
