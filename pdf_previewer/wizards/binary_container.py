# Copyright 2021 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64

from odoo import fields, models


class BinaryContainer(models.TransientModel):
    _name = "binary.container"
    _description = "PDF viewer for workorders"

    binary_field = fields.Binary(string="Binary File")
    name = fields.Char(string="Binary Name")

    def load_binary(self, file):
        binary = base64.b64encode(file)
        self.binary_field = binary
