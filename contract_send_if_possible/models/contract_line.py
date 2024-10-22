import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ContractLine(models.Model):
    _inherit = "contract.line"

    error_occurred = fields.Boolean(
        default=False,
    )

    def _check_recurring_next_date_start_date(self):
        for line in self:
            if line.display_type == "line_section" or not line.recurring_next_date:
                continue
            if line.date_start and line.recurring_next_date:
                if line.date_start > line.recurring_next_date:
                    line.error_occurred = True
                    _logger.error(
                        "Failed to validate recurring date for contract line '%s': "
                        "start date '%s' is after next date '%s'",
                        line.name,
                        line.date_start,
                        line.recurring_next_date,
                    )
                    continue
