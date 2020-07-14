# Copyright 2020 Adrian  - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin',
                'stock.picking']

    signature = fields.Binary('Signature',
                              help='Signature received through the portal.',
                              copy=False, attachment=True)
    signed_by = fields.Char('Signed by',
                            help='Name of the person that signed the SP.',
                            copy=False)

    def has_to_be_signed(self):
        return (self.state == 'waiting' or self.state == 'confirmed' or
                self.state == 'draft')

    def _compute_access_url(self):
        super(StockPicking, self)._compute_access_url()
        for stock_picking in self:
            stock_picking.access_url = '/my/stock/%s' % (stock_picking.id)

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return '%s %s' % (self.picking_type_id.name, self.name)
