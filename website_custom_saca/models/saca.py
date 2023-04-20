
from odoo import _, api, fields, models


class SacaLine(models.Model):
    _inherit = "saca.line"

    def _get_report_base_filename(self):
        self.ensure_one()
        fname = "Saca Form-%s" % self.name
        return fname