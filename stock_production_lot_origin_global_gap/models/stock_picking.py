# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        in_pickings = self.filtered(
            lambda x: x.picking_type_id.code == "incoming")
        for picking in in_pickings:
            lines = picking.move_line_ids_without_package.filtered(
                lambda x: x.lot_name)
            for line in lines:
                if not line.country_id:
                    raise UserError(
                        _("You must enter the origin for the lot: {}").format(
                            line.lot_name))
                if not line.global_gap:
                    raise UserError(
                        _("You must enter the global gap for the lot: "
                          "{}").format(line.lot_name))
        return super(StockPicking, self).button_validate()
