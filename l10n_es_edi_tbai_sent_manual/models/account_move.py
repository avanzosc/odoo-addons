# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    tbai_manual_sent = fields.Boolean(default=False)

    @api.depends(
        "l10n_es_tbai_post_document_id.state",
        "l10n_es_tbai_cancel_document_id.state",
        "tbai_manual_sent",
    )
    def _compute_l10n_es_tbai_state(self):
        result = super()._compute_l10n_es_tbai_state()
        moves = self.filtered(lambda x: x.tbai_manual_sent)
        for move in moves:
            move.l10n_es_tbai_state = "sent"
        return result
