# -*- coding: utf-8 -*-
# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, exceptions, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    quotation_visible = fields.Boolean(related="type_id.quotation_visible",
                                       store=True)
    quotation_confirmation_date = fields.Datetime(string="Quotation "
                                                         "Confirmation Date")
    quotation_rejection_date = fields.Datetime(string="Quotation Rejection "
                                                      "Date")
    quotation_state = fields.Char(string="Quoation State",
                                  compute="_compute_quotation_state")

    @api.constrains('quotation_confirmation_date', 'quotation_rejection_date')
    def template_variant_ids(self):
        if self.quotation_confirmation_date and self.quotation_rejection_date:
            raise exceptions.ValidationError(
                'Confirmation and rejection date can not be filled at the '
                'same time')

    @api.depends('quotation_confirmation_date', 'quotation_rejection_date')
    def _compute_quotation_state(self):
        for sale in self:
            if sale.quotation_rejection_date:
                sale.quotation_state = _('Rejected')
            elif sale.quotation_confirmation_date:
                sale.quotation_state = _('Confirmed')
            else:
                sale.quotation_state = _('Pending')
