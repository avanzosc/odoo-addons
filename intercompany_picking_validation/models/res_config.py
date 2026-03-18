# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    picking_intercompany_validation = fields.Boolean(
        string="When validating picking validate also in the other company",
        config_parameter="intecompany_picking_validation."
        "picking_intercompany_validation",
    )
    picking_intercompany_validation_backorder = fields.Boolean(
        string="When validating picking validate also in the other company",
        config_parameter="intecompany_picking_validation."
        "picking_intercompany_validation_backorder",
    )
