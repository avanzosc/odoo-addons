# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_offer_type = fields.Boolean(
        string='It is an offer type', default=False)
    from_offer_id = fields.Many2one(
        string='From offer', comodel_name='sale.order', copy=False)
    introduction = fields.Text(
        string='Introduction')
    acceptance_date = fields.Date(
        string='Acceptance date', copy=False)
    rejection_date = fields.Date(
        string='Rejection date', copy=False)
    stage = fields.Selection([
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('pending', _('Pending'))],
        string="State")
    sale_ids = fields.One2many(
        string='Sale orders', comodel_name='sale.order',
        inverse_name='from_offer_id')
    count_sale_orders = fields.Integer(
        string='Sale orders', compute='_compute_count_sale_orders')

    def _compute_count_sale_orders(self):
        for sale in self:
            sale.count_sale_orders = len(sale.sale_ids)

    @api.model
    def _default_type_id(self):
        if ('default_is_offer_type' in self.env.context and
                self.env.context.get('default_is_offer_type', False)):
            cond = [('is_offer_type', '=', True)]
            return self.env["sale.order.type"].search(cond, limit=1)
        return super(SaleOrder, self)._default_type_id()

    @api.onchange("type_id")
    def onchange_type_id(self):
        result = super(SaleOrder, self).onchange_type_id()
        for order in self.filtered(lambda x: x.type_id):
            self.is_offer_type = order.type_id.is_offer_type
        return result

    def action_offer_to_quotation(self):
        for offer in self.filtered(lambda x: x.is_offer_type):
            cond = [('is_offer_type', '=', False)]
            normal_type = self.env["sale.order.type"].search(cond, limit=1)
            default = {'type_id': normal_type.id,
                       'is_offer_type': normal_type.is_offer_type,
                       'from_offer_id': offer.id}
            offer.copy(default)

    @api.onchange("stage")
    def onchange_stage(self):
        for order in self:
            vals = {'acceptance_date': False,
                    'rejection_date': False}
            if order.stage == 'accepted':
                vals['acceptance_date'] = fields.Date.context_today(self)
            if order.stage == 'rejected':
                vals['rejection_date'] = fields.Date.context_today(self)
            order.write(vals)

    def action_view_sale_orders(self):
        self.ensure_one()
        action = self.env.ref(
            "sale_order_offer_version.action_view_all_sale_orders")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("id", "in", self.mapped('sale_ids').ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({
            "domain": domain,
        })
        return action_dict
