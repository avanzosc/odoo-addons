# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    supplier_zone = fields.Many2one(
        string='Supplier zone',
        comodel_name='partner.delivery.zone',
        related='name.partner_zone_id')
    supplier_state = fields.Many2one(
        string='Supplier state',
        comodel_name='res.country.state',
        related='name.state_id')
    supplier_city = fields.Char(
        string='Supplier city',
        related='name.city')
