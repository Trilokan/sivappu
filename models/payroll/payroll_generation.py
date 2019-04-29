# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions

PROGRESS_INFO = [('draft', 'Draft'), ('generated', 'Generated')]


# payroll Generation
class PayrollGeneration(models.Model):
    _name = "payroll.generation"
    _inherit = "mail.thread"
    _rec_name = "month_id"

    month_id = fields.Many2one(comodel_name="month.attendance", string="Month", required=True)
    person_ids = fields.Many2many(comodel_name="arc.person", string="Employee")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")

    @api.multi
    def trigger_generate(self):
        recs = self.person_ids
        if not recs:
            raise exceptions.ValidationError("Error! No Employees found")

        for rec in recs:
            data = {"person_id": rec.id,
                    "month_id": self.month_id.id,
                    "progress": "draft"}

            payslip_id = self.env["pay.slip"].create(data)
            payslip_id.generate_payslip()

        self.write({"progress": "generated"})
