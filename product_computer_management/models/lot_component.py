# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class LotComponent(models.Model):
    _name = "lot.component"
    _description = "Lot Component"

    name = fields.Char(string="Name", required=True, copy=False)
    lot_id = fields.Many2one(
        string="Lot/Serial Nº", comodel_name="stock.production.lot"
    )
    didx = fields.Integer(string="Didx")
    manufacturer_id = fields.Many2one(string="Manufacturer", comodel_name="res.partner")
    model_id = fields.Many2one(string="Model", comodel_name="product.model")
    serial = fields.Char(string="Serial")
    size = fields.Char(string="Size")
    speed_id = fields.Many2one(string="Speed", comodel_name="speed")
    info1 = fields.Text(string="Info. 1")
    info2 = fields.Text(string="Info. 2")
    info3 = fields.Text(string="Info. 3")
    secured = fields.Char(string="Secured")
    tested = fields.Selection(
        selection=[("ok", "OK"), ("no_ok", "No OK")], string="Tested"
    )
