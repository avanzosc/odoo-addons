# Copyright (C) 2013 Obertix Free Software Solutions (<http://obertix.net>).
#                    cubells <info@obertix.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class StockTransferDetailsItems(models.TransientModel):
    _inherit = 'stock.transfer_details_items'
    _description = 'Picking wizard items'

    @api.multi
    def split_all_quantities(self):
        for det in self:
            while det.quantity > 1:
                det.quantity = (det.quantity - 1)
                new_id = det.copy(context=self.env.context)
                new_id.quantity = 1
                new_id.packop_id = False
        if self and self[0]:
            return self[0].transfer_id.wizard_view()
