# -*- coding: utf-8 -*-

from odoo import models, fields, api

REPORT_LIST = [("stock_adjustment", "Stock Adjustment"),
               ("store_request", "Store Request"),
               ("store_issue", "Store Issue"),
               ("store_return", "Store Return"),
               ("store_accept", "Store Accept")]


class ReportStockAnalysis(models.TransientModel):
    _name = "report.stock.analysis"

    from_date = fields.Date(string="Fom Date", required=True)
    till_date = fields.Date(string="Till Date", required=True)
    report_list = fields.Selection(selection=REPORT_LIST, string="Report List")
    product_id = fields.Many2one(comodel_name="arc.product", string="Product")

    def get_store_request_records(self):
        recs = self.env["store.request.detail"].search([("request_id.date", ">=", self.from_date),
                                                        ("request_id.date", "<=", self.till_date),
                                                        ("product_id", "=", self.product_id.id)])

        report = []
        for rec in recs:
            report.append({"Date": rec.date,
                           "Name": rec.request_id.name,
                           "Department": rec.request_id.department_id.name,
                           "Request by": rec.request_id.requested_by.name,
                           "Product": rec.product_id.name,
                           "UOM": rec.product_id.uom_id.name,
                           "Description": rec.description,
                           "Requested Quantity": rec.requested_quantity,
                           "Approved Quantity": rec.approved_quantity})

        return report

    def get_store_issue_records(self):
        recs = self.env["store.issue.detail"].search([("issue_id.date", ">=", self.from_date),
                                                      ("issue_id.date", "<=", self.till_date),
                                                      ("product_id", "=", self.product_id.id)])

        report = []
        for rec in recs:
            report.append({"Date": rec.date,
                           "Name": rec.issue_id.name,
                           "Department": rec.issue_id.department_id.name,
                           "Issued by": rec.issue_id.issue_by.name,
                           "Product": rec.product_id.name,
                           "UOM": rec.product_id.uom_id.name,
                           "Description": rec.description,
                           "Requested Quantity": rec.requested_quantity,
                           "Issued Quantity": rec.issue_quantity})

        return report

    def get_store_return_records(self):
        recs = self.env["store.return.detail"].search([("return_id.date", ">=", self.from_date),
                                                       ("return_id.date", "<=", self.till_date),
                                                       ("product_id", "=", self.product_id.id)])

        report = []
        for rec in recs:
            report.append({"Date": rec.date,
                           "Name": rec.return_id.name,
                           "Department": rec.return_id.department_id.name,
                           "Return by": rec.return_id.returned_by.name,
                           "Product": rec.product_id.name,
                           "UOM": rec.product_id.uom_id.name,
                           "Description": rec.description,
                           "Returned Quantity": rec.returned_quantity,
                           "Approved Quantity": rec.approved_quantity})

        return report

    def get_store_accept_records(self):
        recs = self.env["store.accept.detail"].search([("accept_id.date", ">=", self.from_date),
                                                       ("accept_id.date", "<=", self.till_date),
                                                       ("product_id", "=", self.product_id.id)])

        report = []
        for rec in recs:
            report.append({"Date": rec.date,
                           "Name": rec.accept_id.name,
                           "Department": rec.accept_id.department_id.name,
                           "Accept by": rec.accept_id.issue_by.name,
                           "Product": rec.product_id.name,
                           "UOM": rec.product_id.uom_id.name,
                           "Description": rec.description,
                           "Requested Quantity": rec.returned_quantity,
                           "Issued Quantity": rec.accept_quantity})

        return report

    @api.multi
    def trigger_stock_analysis(self):
        if self.report_list == "store_request":
            recs = self.get_store_request_records()
        elif self.report_list == "store_issue":
            recs = self.get_store_issue_records()
        elif self.report_list == "store_return":
            recs = self.get_store_return_records()
        elif self.report_list == "store_accept":
            recs = self.get_store_accept_records()

        print recs
