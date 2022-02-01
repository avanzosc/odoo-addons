# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    partner_contact_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contact",
        readonly=False,
        states={"purchase": [("readonly", True)],
                "done": [("readonly", True)],
                "cancel": [("readonly", True)]},
    )
