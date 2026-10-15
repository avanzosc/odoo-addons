# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    modules = fields.Char(
        store=True,
        readonly=True,
    )
