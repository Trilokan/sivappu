# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Account(models.Model):
    _name = "arc.account"

    name = fields.Char(string="Name", required=True)
    account_uid = fields.Char(string="Code", readonly=True)

    _sql_constraints = [("account_uid", "unique(account_uid)", "Account Code must be unique")]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.account_uid, record.name)
            result.append((record.id, name))
        return result

    @api.model
    def create(self, vals):
        vals["account_uid"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(Account, self).create(vals)
