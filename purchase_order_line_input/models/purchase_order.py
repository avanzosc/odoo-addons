# Copyright 2018 Tecnativa - Carlos Dauden
# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    lines_count = fields.Integer(string="Lines Count",
                                 compute="_compute_order_lines", store=True)

    @api.depends('order_line')
    def _compute_order_lines(self):
        for line in self:
            line.lines_count = len(line.order_line)

    @api.multi
    def action_view_lines(self):
        action = self.env.ref(
            'purchase_order_line_input.action_purchase_order_line_input')
        result = action.read()[0]
        create_bill = self.env.context.get('create_bill', False)
        # override the context to get rid of the default filtering
        result['context'] = {
            'type': 'in_invoice',
            'default_order_id': self.id,
            'default_currency_id': self.currency_id.id,
            'default_company_id': self.company_id.id,
            'company_id': self.company_id.id
        }
        # choose the view_mode accordingly
        result['domain'] = "[('order_id', '=', {})]".format(self.id)
        return result


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    user_id = fields.Many2one(related='order_id.user_id', store=True,
                              string='Salesperson', readonly=True)

    @api.model
    def create(self, vals):
        if not vals.get('order_id', False):
            purchase_order = self.env['purchase.order']
            new_po = purchase_order.new({
                'partner_id': vals.pop('partner_id'),
            })
            for onchange_method in new_po._onchange_methods['partner_id']:
                onchange_method(new_po)
            order_data = new_po._convert_to_write(new_po._cache)
            vals['order_id'] = new_po.create(order_data).id
        return super().create(vals)

    @api.multi
    def action_purchase_order_form(self):
        self.ensure_one()
        action = self.env.ref('purchase.purchase_form_action')
        form = self.env.ref('purchase.purchase_order_form')
        action = action.read()[0]
        action['views'] = [(form.id, 'form')]
        action['res_id'] = self.order_id.id
        return action
