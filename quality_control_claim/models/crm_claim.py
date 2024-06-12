# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class CrmClaim(models.Model):
    _inherit = "crm.claim"

    def _selection_model(self):
        result = super()._selection_model()
        result.extend([("qc.inspection", "Quality control inspection")])
        return result
