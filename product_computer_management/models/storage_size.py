# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StorageSize(models.Model):
    _name = "storage.size"
    _description = "Storage Size"

    name = fields.Char(string="Name", required=True, copy=False)
