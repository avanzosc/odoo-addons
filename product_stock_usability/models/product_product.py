# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    move_line_ids = fields.One2many(
        string="Product Move Lines",
        comodel_name="stock.move.line",
        inverse_name="product_id",
        copy=False,
    )
    root_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Root Category",
        related="categ_id.root_category_id",
        store=True,
    )
    parent_category_id = fields.Many2one(
        comodel_name="product.category",
        string="Parent Category",
        related="categ_id.parent_id",
        store=True,
    )
    show_incoming_qty_status_button = fields.Boolean(
        compute="_compute_show_qty_status_button"
    )
    show_outgoing_qty_status_button = fields.Boolean(
        compute="_compute_show_qty_status_button"
    )

    @api.depends("product_tmpl_id")
    def _compute_show_qty_status_button(self):
        result = super()._compute_show_qty_status_button()
        for product in self:
            product.show_incoming_qty_status_button = (
                product.product_tmpl_id.show_incoming_qty_status_button
            )
            product.show_outgoing_qty_status_button = (
                product.product_tmpl_id.show_outgoing_qty_status_button
            )
        return result
