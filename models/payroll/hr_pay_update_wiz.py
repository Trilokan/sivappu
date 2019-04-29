# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import datetime

PROGRESS_INFO = [('draft', 'Draft'), ('generated', 'Generated')]
PAY_TYPE = [('allowance', 'Allowance'), ('deduction', 'Deduction')]
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
CURRENT_TIME_INDIA = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Pay Update
class HRPayWiz(models.TransientModel):
    _name = "hr.pay.wizard"

    person_id = fields.Many2one(comodel_name="arc.person", string="Employee",
                                default=lambda self: self.env.context.get('person_id', False))
    basic = fields.Float(string="Basic",
                         default=lambda self: self.env.context.get('basic', False))
    structure_id = fields.Many2one(comodel_name="salary.structure", string="Salary Structure",
                                   default=lambda self: self.env.context.get('structure_id', False))

    def trigger_pay_update(self):
        writter = "Employee Pay Updated by {0} on {1}".format(self.person_id.name, CURRENT_TIME_INDIA)

        hr_pay_id = self.env["hr.pay"].search([("person_id", "=", self.person_id.id)])
        hr_pay_id.write({"basic": self.basic,
                         "structure_id": self.structure_id.id,
                         "writter": writter})
