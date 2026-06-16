# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    egg = fields.Boolean(string="Egg", related="product_id.egg", store=True)
    batch_location_id = fields.Many2one(
        string="Mother Location",
        comodel_name="stock.location",
        related="batch_id.location_id",
        store=True,
    )
    batch_category_type_id = fields.Many2one(
        string="Batch Section",
        comodel_name="category.type",
        related="batch_location_id.type_id",
        store=True,
    )
    product_category_type_id = fields.Many2one(
        string="Product Category Section",
        comodel_name="category.type",
        related="product_category_id.type_id",
        store=True,
    )
    show_in_report = fields.Boolean(
        string="Show in Report", related="picking_id.show_in_report", store=True
    )
    commercial_partner_id = fields.Many2one(
        comodel_name="res.partner",
        related="picking_partner_id.commercial_partner_id",
        store=True,
    )
    contact_sale_type_id = fields.Many2one(
        comodel_name="sale.order.type",
        compute="_compute_contact_sale_type_id",
        store=True,
    )

    @api.depends("company_id", "picking_partner_id")
    def _compute_contact_sale_type_id(self):
        for line in self:
            partner = line.picking_partner_id
            if partner:
                sale_type = partner.with_company(line.company_id).sale_type
                if sale_type:
                    line.contact_sale_type_id = sale_type.id
