# -*- coding: utf-8 -*-
# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ProductSupplierinfoCertification(models.Model):
    _name = "product.supplierinfo.certification"
    _description = "Certifications In Supplier Pricelist"
    _order = "name asc"

    name = fields.Char(
        string="Description", required=True
    )
