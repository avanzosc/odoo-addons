import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        context = dict(self.env.context)
        context["no_update_picking_ids"] = self.ids

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

        result = super(StockPicking, self.with_context(context)).button_validate()

        try:
            if original_custom_date_done:
                for picking_id, date_value in original_custom_date_done.items():
                    self._cr.execute(
                        """
                        UPDATE stock_picking
                        SET date_done = %s
                        WHERE id = %s
                        """,
                        (date_value if date_value else None, picking_id),
                    )

            if original_scheduled_date:
                for picking_id, date_value in original_scheduled_date.items():
                    self._cr.execute(
                        """
                        UPDATE stock_picking
                        SET scheduled_date = %s
                        WHERE id = %s
                        """,
                        (date_value if date_value else None, picking_id),
                    )

        except Exception as e:
            _logger.error("Error updating picking dates: %s", str(e))
            raise

        return result

    @api.depends("move_ids.state", "move_ids.date", "move_type")
    def _compute_scheduled_date(self):
        """Override the `_compute_scheduled_date` method to prevent automatic update
        of the `scheduled_date` when a picking is validated."""
        for picking in self:
            # Save the original value of `scheduled_date`
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

            # Restore `scheduled_date` if it hasn't changed
            if picking.scheduled_date == original_scheduled_date:
                picking.scheduled_date = original_scheduled_date
