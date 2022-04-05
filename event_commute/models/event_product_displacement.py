# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields
from odoo.addons import decimal_precision as dp


class EventProductDisplacement(models.Model):
    _name = 'event.product.displacement'
    _description = 'Products for event displacement'

    event_id = fields.Many2one(
        string='Event', comodel_name='event.event')
    project_id = fields.Many2one(
        string='Project', comodel_name='project.project',
        related='sale_order_line_id.project_id', store=True)
    task_id = fields.Many2one(
        string='Task', comodel_name='project.task',
        related='sale_order_line_id.task_id', store=True)
    sale_order_id = fields.Many2one(
        string='Sale order', comodel_name='sale.order',
        related='sale_order_line_id.order_id', store=True)
    sale_order_line_id = fields.Many2one(
        string='Sale order line', comodel_name='sale.order.line')
    product_id = fields.Many2one(
        string='Product', comodel_name='product.product')
    sale_price_unit = fields.Float(
        string='Sale price', digits=dp.get_precision('Product Price'),
        related='sale_order_line_id.price_unit', store=True)
    standard_price = fields.Float(
        string='Cost', digits=dp.get_precision('Product Price'))
