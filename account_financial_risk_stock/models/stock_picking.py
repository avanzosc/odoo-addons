# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    risk_exception = fields.Boolean(
        string="Risk Exception", related="partner_id.risk_exception", store=True
    )

    def button_validate(self):
        for picking in self.filtered(lambda x: x.picking_type_id.code == "outgoing"):
            if (
                picking.partner_id.block_picking_risk
                and picking.partner_id.risk_exception
            ):
                error = _(
                    "The client: %(customer_name)s has blocked the issuance of "
                    "delivery notes due to risk limits. Contact with administration."
                ) % {
                    "customer_name": picking.partner_id.name,
                }
                raise ValidationError(error)
        return super().button_validate()
