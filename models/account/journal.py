# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Journal(models.Model):
    _name = "arc.journal"

    name = fields.Char(string="Name", required=True)
    journal_uid = fields.Char(string="Code", required=True)

    _sql_constraints = [("name", "unique(name)", "Journal must be unique"),
                        ("journal_uid", "unique(journal_uid)", "Journal Code must be unique")]
