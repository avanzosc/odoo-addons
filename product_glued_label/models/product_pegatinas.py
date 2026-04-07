# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    codigobarras = fields.Binary("Small Box")
    pegatinacaja = fields.Binary("Big Box")
