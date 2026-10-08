# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

# Not a legal figure -- the DeCA itself is retained indefinitely (no
# apartado sets a ceiling), but keeping raw IP addresses forever alongside
# it is unnecessary data hoarding once we're well past the one-year
# minimum retention window (see the compliance matrix in README.md). Past
# that point the document itself is still all that's legally required;
# the granular per-request evidence isn't.
ACCESS_LOG_RETENTION_DAYS = 365


class StockPickingBatchDecaAccessLog(models.Model):
    _name = "stock.picking.batch.deca.access.log"
    _description = "DeCA Public Access Log"
    _order = "access_date desc, id desc"

    picking_batch_id = fields.Many2one(
        comodel_name="stock.picking.batch",
        required=True,
        ondelete="cascade",
        index=True,
    )
    access_date = fields.Datetime(
        string="Date", required=True, default=fields.Datetime.now, readonly=True
    )
    ip_address = fields.Char(string="IP Address", readonly=True)
    method = fields.Char(readonly=True)
    status_code = fields.Integer(string="Status", readonly=True)

    @api.model
    def _cron_purge_old(self):
        cutoff = fields.Datetime.subtract(
            fields.Datetime.now(), days=ACCESS_LOG_RETENTION_DAYS
        )
        self.search([("access_date", "<", cutoff)]).unlink()
