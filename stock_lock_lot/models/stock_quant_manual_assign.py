from odoo import api, models


class StockQuantManualAssign(models.TransientModel):
    _inherit = "stock.quant.manual.assign"

    @api.model
    def _get_domain(self):
        domain = super()._get_domain()
        stage_blocked_ids = (
            self.env["stock.lot.stage"].search([("stage_blocking", "=", True)]).ids
        )
        domain.append(("lot_id.stage_id", "not in", stage_blocked_ids))
        return domain
