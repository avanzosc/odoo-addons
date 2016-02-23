# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class ProcurementOrderpointCompute(models.TransientModel):
    _inherit = 'procurement.orderpoint.compute'

    locations = fields.Many2many('stock.location', string='Locations')
    categories = fields.Many2many('product.category', string='Categories')

    @api.multi
    def procure_calculation(self):
        self.ensure_one()
        return super(ProcurementOrderpointCompute, self.with_context(
            locations_filter=self.locations,
            categories_filter=self.categories)).procure_calculation()
