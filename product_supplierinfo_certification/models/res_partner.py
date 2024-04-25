# -*- coding: utf-8 -*-
# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    certification_id = fields.Many2one(
        string="Supplier qualification",
        comodel_name="product.supplierinfo.certification",
        copy=False
    )
