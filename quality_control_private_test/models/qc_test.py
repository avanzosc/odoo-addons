# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QcTest(models.Model):
    _inherit="qc.test"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template", string='Private product test')