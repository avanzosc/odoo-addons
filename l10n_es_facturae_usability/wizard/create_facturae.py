# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class CreateFacturae(models.TransientModel):
    _inherit = "create.facturae"

    @api.multi
    def create_facturae_file(self):
        invoice_ids = self.env.context.get("active_ids", [])
        if not invoice_ids or len(invoice_ids) == 1:
            return super(CreateFacturae, self).create_facturae_file()
        for invoice_id in invoice_ids:
            super(CreateFacturae, self.with_context(
                active_ids=[invoice_id])).create_facturae_file()
