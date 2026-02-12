# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    agreement_id = fields.Many2one(
        comodel_name="agreement",
        string="Agreement",
        ondelete="restrict",
        readonly=True,
        copy=False,
        help="This field is a technical field",
    )

    def _key_assign_picking(self):
        self.ensure_one()
        keys = super()._key_assign_picking()
        keys += (self.agreement_id,)
        return keys

    def _get_new_picking_values(self):
        """return create values for new picking that will be linked with group
        of moves in self.
        """
        values = super()._get_new_picking_values()
        values.update(
            {
                "agreement_id": self.mapped("agreement_id").id,
            }
        )
        return values
