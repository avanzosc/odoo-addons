from odoo import fields, models


class ResGroups(models.Model):
    _inherit = "res.groups"

    view_purchase_tab = fields.Boolean(
        default=True,
    )
