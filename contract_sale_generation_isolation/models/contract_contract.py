# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ContractContract(models.Model):
    _inherit = "contract.contract"

    sale_generation_exception = fields.Boolean(
        string="Sale Generation Error",
        copy=False,
        help=(
            "Automatically set when the recurring sale order generation "
            "for this contract fails. While set, the contract is skipped "
            "by the daily cron."
        ),
    )
    sale_generation_exception_message = fields.Text(
        string="Error Detail",
        copy=False,
        readonly=True,
    )
    sale_generation_exception_date = fields.Datetime(
        string="Error Date",
        copy=False,
        readonly=True,
    )

    @api.model
    def _get_contracts_to_invoice_domain(self, date_ref=None):
        domain = super()._get_contracts_to_invoice_domain(date_ref=date_ref)
        return domain + [("sale_generation_exception", "=", False)]

    def _recurring_create_sale(self, date_ref=False):
        if len(self) > 1:
            sale_orders = self.env["sale.order"]
            errors = 0
            for contract in self:
                already_flagged = contract.sale_generation_exception
                sale_orders |= contract._recurring_create_sale(date_ref=date_ref)
                if not already_flagged and contract.sale_generation_exception:
                    errors += 1
            if errors:
                _logger.info(
                    "Recurring sale generation: %s out of %s contract(s) "
                    "failed and were flagged for review.",
                    errors,
                    len(self),
                )
            return sale_orders

        self.ensure_one()
        if self.sale_generation_exception:
            return self.env["sale.order"]
        self.env.cr.commit()  # pylint: disable=invalid-commit
        try:
            sale_orders = super()._recurring_create_sale(date_ref=date_ref)
        except Exception as error:  # noqa: BLE001
            self.env.cr.rollback()
            _logger.exception(
                "Error generating the recurring sale order for contract %s",
                self.display_name,
            )
            self._mark_sale_generation_exception(error)
            sale_orders = self.env["sale.order"]
        self.env.cr.commit()  # pylint: disable=invalid-commit
        return sale_orders

    def _mark_sale_generation_exception(self, error):
        self.ensure_one()
        self.write(
            {
                "sale_generation_exception": True,
                "sale_generation_exception_message": str(error),
                "sale_generation_exception_date": fields.Datetime.now(),
            }
        )
        self._notify_sale_generation_exception()

    def _get_sale_generation_exception_responsible(self):
        self.ensure_one()
        param = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("contract_sale_generation_isolation.responsible_user_id")
        )
        user = self.env["res.users"]
        if param:
            user = self.env["res.users"].browse(int(param)).exists()
        return user or self.user_id

    def _notify_sale_generation_exception(self):
        self.ensure_one()
        user = self._get_sale_generation_exception_responsible()
        if not user:
            return
        self.activity_schedule(
            "mail.mail_activity_data_todo",
            summary=_("Error generating the recurring sale order"),
            note=self.sale_generation_exception_message,
            user_id=user.id,
        )

    def action_reset_sale_generation_exception(self):
        self.write(
            {
                "sale_generation_exception": False,
                "sale_generation_exception_message": False,
                "sale_generation_exception_date": False,
            }
        )
