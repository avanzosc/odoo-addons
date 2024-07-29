# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, fields, models

WARNING_MESSAGE = [
    ("no-message", _("No Message")),
    ("warning", _("Warning")),
    ("block", _("Blocking Message")),
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    out_picking_warn = fields.Selection(
        selection=WARNING_MESSAGE,
        required=True,
        string="Out picking line",
        default="no-message",
        copy=False,
    )
    out_picking_warn_msg = fields.Text(
        string="Message for out picking line", copy=False
    )
    in_picking_warn = fields.Selection(
        selection=WARNING_MESSAGE,
        required=True,
        string="In picking line",
        default="no-message",
        copy=False,
    )
    in_picking_warn_msg = fields.Text(string="Message for in picking line", copy=False)
