# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Grade(models.Model):
    _name = "grade"
    _description = "Grade"

    name = fields.Char(string="Name", required=True, copy=False)
    tested = fields.Selection(
        selection=[("ok", "OK"), ("no_ok", "No OK")],
        string="Tested",
        requited=True,
        copy=False,
    )
