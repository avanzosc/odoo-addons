# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    is_mould = fields.Boolean(related="product_id.product_tmpl_id.is_mould")
    mould_id = fields.Many2one(
        comodel_name="product.mould",
        string="Mould",
        domain=[("type", "=", "mould")],
    )
    manufacturing_year = fields.Integer()
    modification_year = fields.Integer()
    mould_length_mm = fields.Float(string="Mould Length (mm)")
    mould_width_mm = fields.Float(string="Mould Width (mm)")
    press_piston_pressure = fields.Float()
    mould_area_cm2 = fields.Float(string="Mould Area (cm²)")
    piston_area_cm2 = fields.Float(string="Piston Area (cm²)")
    pressure_kg_cm2 = fields.Float(string="Pressure (kg/cm²)")
