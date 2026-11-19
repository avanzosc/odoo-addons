# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_origin_location(self):
        origin_partner = (
            self.picking_id.picking_type_id.warehouse_id.partner_id
            or self.picking_id.company_id.partner_id
        )
        return self._format_address_inline(origin_partner)

    def _get_destination_location(self):
        return self._format_address_inline(self.picking_id.partner_id)

    @api.model
    def _format_address_inline(self, partner):
        """partner.contact_address comes back multi-line (one address
        component per line), fine for a free block of text but not for a
        table cell -- the Envío table (art. 6.c) needs origin/destination
        to stay compact since it's next to Naturaleza/Peso/Fecha on the
        same row. Comma-joins it into a single line instead, and drops a
        trailing "España" line: every line a DeCA actually covers is
        domestic by definition (an international one never reaches this
        table at all -- l10n_es_deca_status is "not_required" for those
        instead), so repeating the country on every single row would be
        pure noise, not information a road inspector needs.
        """
        if not partner or not partner.contact_address:
            return ""
        lines = [
            line.strip()
            for line in partner.contact_address.splitlines()
            if line.strip()
        ]
        if lines and partner.country_id and partner.country_id.code == "ES":
            lines = lines[:-1]
        return ", ".join(lines)
