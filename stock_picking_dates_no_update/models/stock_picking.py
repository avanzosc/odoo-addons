import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        result = super(
            StockPicking, self.with_context(no_update_picking_ids=self.ids)
        ).button_validate()

        original_custom_date_done = {
            picking.id: (
                picking.custom_date_done.replace(tzinfo=None)
                if picking.custom_date_done
                else False
            )
            for picking in self
        }

        original_scheduled_date = {
            picking.id: (
                picking.scheduled_date.replace(tzinfo=None)
                if picking.scheduled_date
                else False
            )
            for picking in self
        }

        try:
            self.update_picking_dates_write(
                original_custom_date_done, original_scheduled_date
            )
        except Exception as e:
            _logger.error("Error updating picking dates with SQL: %s", str(e))
            raise

        return result

    def update_picking_dates_write(
        self, original_custom_date_done, original_scheduled_date
    ):
        try:
            for picking in self.with_context(write_dates_with_no_error=True):
                updates = {}
                if picking.id in original_custom_date_done:
                    updates["date_done"] = (
                        original_custom_date_done[picking.id] or False
                    )
                if picking.id in original_scheduled_date:
                    updates["scheduled_date"] = (
                        original_scheduled_date[picking.id] or False
                    )
                if updates:
                    picking.write(updates)

        except Exception as e:
            _logger.error("Error updating picking dates with write: %s", str(e))
            raise

    def _set_scheduled_date(self):
        try:
            res = super()._set_scheduled_date()
        except Exception as e:
            _logger.error("Error occurred while setting the scheduled date: %s", str(e))
            if not self.env.context.get("write_dates_with_no_error", False):
                raise
            else:
                return res

    @api.depends("move_ids.state", "move_ids.date", "move_type")
    def _compute_scheduled_date(self):
        """Override the `_compute_scheduled_date` method to prevent automatic update
        of the `scheduled_date` when a picking is validated."""
        for picking in self:
            original_scheduled_date = picking.scheduled_date

            moves_dates = picking.move_ids.filtered(
                lambda move: move.state not in ("done", "cancel")
            ).mapped("date")
            if picking.move_type == "direct":
                picking.scheduled_date = min(
                    moves_dates, default=picking.scheduled_date or fields.Datetime.now()
                )
            else:
                picking.scheduled_date = max(
                    moves_dates, default=picking.scheduled_date or fields.Datetime.now()
                )

            if picking.scheduled_date == original_scheduled_date:
                picking.scheduled_date = original_scheduled_date
