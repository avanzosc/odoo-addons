# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import api, fields, models


class PurchaseOrderCondition(models.Model):
    _name = 'purchase.order.condition'
    _inherit = ['order.condition']
    _description = 'Purchase Order Condition'
    _order = 'condition_id, purchase_id'

    purchase_id = fields.Many2one(
        comodel_name='purchase.order', string='Purchase Order', required=True)

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        results = []
        for record in self:
            super(PurchaseOrderCondition, record).name_get()
            results.append(
                (record.id, '[{}] {}'.format(record.purchase_id.name,
                                             record.condition_id.name)))
        return results
