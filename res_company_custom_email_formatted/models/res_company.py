import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

    default_email_formatted_company = fields.Char(
        "Default Email Formatted",
        help="Specify the default email address format to display\
            in the 'From' field of outgoing emails for this company.",
    )

    @api.depends(
        "partner_id.email_formatted",
        "catchall_formatted",
        "default_email_formatted_company",
    )
    def _compute_email_formatted(self):
        for company in self:
            _logger.info(f"Processing company: {company.name} (ID: {company.id})")

            if company.default_email_formatted_company:
                _logger.info(
                    f"Custom email format found: {company.default_email_formatted_company}"
                )
                company.email_formatted = company.default_email_formatted_company
                _logger.info(f"Set custom email format: {company.email_formatted}")
            else:
                _logger.info("No custom email format found, using default")
                super(ResCompany, company)._compute_email_formatted()
                _logger.info(f"Used default email format: {company.email_formatted}")

    @api.onchange("default_email_formatted_company")
    def _onchange_default_email_formatted_company(self):
        for company in self:
            _logger.info(
                f"Default email format changed for company: {company.name} (ID: {company.id})"
            )
            company._compute_email_formatted()
