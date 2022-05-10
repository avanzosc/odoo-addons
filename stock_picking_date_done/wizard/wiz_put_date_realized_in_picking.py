# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class WizPutDateRealizedInPicking(models.TransientModel):
    _name = 'wiz.put.date.realized.in.picking'
    _description = 'Wizard for put date realized in picking.'

    custom_date_done = fields.Datetime(
        string='Date realized', required=True)

    def action_put_date_realized_in_picking(self):
        self.ensure_one()
        if self.custom_date_done:
            pickings = self.env['stock.picking'].browse(
                self.env.context.get('active_ids'))
            pickings = pickings.filtered(
                lambda x: x.state in ('done', 'cancel'))
            for picking in pickings:
                picking.custom_date_done = self.custom_date_done
                if picking.move_lines:
                    picking.move_lines.write({'date': self.custom_date_done})
                if picking.move_line_ids:
                    picking.move_line_ids.write({'date': self.custom_date_done})
