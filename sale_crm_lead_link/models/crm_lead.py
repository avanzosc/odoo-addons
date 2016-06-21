# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    @api.multi
    @api.depends('sale_ids', 'sale_ids.state', 'sale_ids.order_line')
    def _compute_sale_lines(self):
        for record in self:
            record.sale_lines = record.mapped('sale_ids.order_line')

    sale_ids = fields.One2many(comodel_name='sale.order',
                               inverse_name='lead_id', string='Sales')
    sale_lines = fields.Many2many(comodel_name='sale.order.line',
                                  compute="_compute_sale_lines",
                                  string="Sale Lines")

    @api.multi
    def write(self, vals):
        sale_obj = self.env['sale.order']
        res = super(CrmLead, self).write(vals)
        if 'ref' in vals:
            for record in self:
                ref = vals.get('ref').split(',')
                if ref[0] == 'sale.order':
                    sale = sale_obj.browse(int(ref[1]))
                    sale.lead_id = record.id
        return res
