# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def onchange_template_id(self, template_id, partner=False,
                             fiscal_position=False, order_line=False):
        if not template_id:
            return {}
        if not partner:
            raise exceptions.Warning(_('You must enter the customer'))
        data = {}
        lines = [(6, 0, [])]
        for line in order_line or []:
            if line[0] == 6 and line[1] == 0 and line[2]:
                for line_id in line[2]:
                    lines.append((4, line_id))
            elif line[0] == 0 and line[1] == 0:
                lines.append(line)
        res = super(SaleOrder, self).onchange_template_id(
            template_id, partner=partner, fiscal_position=fiscal_position)
        value = res.get('value')
        if 'note' in value and value.get('note'):
            data['note'] = value.get('note')
        if ('website_description' in value and
                value.get('website_description')):
            data['website_description'] = value.get('website_description')
        if ('validity_date' in value and value.get('validity_date')):
            data['validity_date'] = value.get('validity_date')
        if ('options' in value and value.get('options')):
            data['options'] = value.get('options')
        order_lines = []
        if ('order_line' in value and value.get('order_line')):
            order_lines = value.get('order_line')
        for line in order_lines:
            if line[0] != 5 and line[0] == 0 and line[1] == 0:
                lines.append(line)
            elif line[0] != 5 and line[0] == 6 and line[2]:
                for line_id in line[2]:
                    lines.append((4, line_id))
        data['order_line'] = lines
        return {'value': data}
