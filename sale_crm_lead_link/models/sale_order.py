# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    lead_id = fields.Many2one(comodel_name='crm.lead', string='Lead')
