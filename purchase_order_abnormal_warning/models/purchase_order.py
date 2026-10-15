from odoo import _, api, fields, models
from odoo.tools import format_date


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    abnormal_amount_warning = fields.Text(compute="_compute_abnormal_warnings")
    abnormal_date_warning = fields.Text(compute="_compute_abnormal_warnings")

    @api.depends("partner_id", "date_order", "amount_total")
    def _compute_abnormal_warnings(self):
        """Assign warning fields based on historical data.
        The last purchase orders (between 10 and 30) are used to compute
        the normal distribution.
        """
        if self.env.context.get("disable_abnormal_purchase_detection"):
            draft_orders = self.browse()
        else:
            draft_orders = self.filtered(
                lambda po: po.state in ("draft", "sent", "to approve")
                and po.amount_total
                and po.partner_id
            )
        other_orders = self - draft_orders
        other_orders.abnormal_amount_warning = False
        other_orders.abnormal_date_warning = False
        if not draft_orders:
            return
        draft_orders.flush_recordset(
            [
                "partner_id",
                "date_order",
                "amount_total",
                "company_id",
                "currency_id",
                "state",
            ]
        )
        today = fields.Date.context_today(self)
        self.env.cr.execute(
            """
            WITH previous_orders AS (
                  SELECT this.id,
                         other.date_order,
                         other.amount_total,
                         EXTRACT(
                             EPOCH FROM (
                                 LAG(other.date_order) OVER purchase_order
                                 - other.date_order
                             )
                         ) / 86400.0 AS date_diff
                    FROM purchase_order this
                    JOIN purchase_order other
                      ON other.partner_id = this.partner_id
                     AND other.company_id = this.company_id
                     AND other.currency_id = this.currency_id
                   WHERE other.state = 'purchase'
                     AND other.date_order <= COALESCE(
                         this.date_order,
                         %(today)s
                     )
                     AND this.id = ANY(%(order_ids)s)
                     AND this.id != other.id
                  WINDOW purchase_order AS (
                      PARTITION BY this.id
                      ORDER BY other.date_order DESC
                  )
            ), stats AS (
                  SELECT id,
                         (MAX(date_order) OVER purchase_order)::date
                             AS last_order_date,
                         AVG(date_diff) OVER purchase_order
                             AS date_diff_mean,
                         STDDEV_SAMP(date_diff) OVER purchase_order
                             AS date_diff_deviation,
                         AVG(amount_total) OVER purchase_order
                             AS amount_mean,
                         STDDEV_SAMP(amount_total) OVER purchase_order
                             AS amount_deviation,
                         ROW_NUMBER() OVER purchase_order
                             AS row_number
                    FROM previous_orders
                  WINDOW purchase_order AS (
                      PARTITION BY id
                      ORDER BY date_order DESC
                  )
            )
              SELECT id,
                     last_order_date,
                     date_diff_mean,
                     date_diff_deviation,
                     amount_mean,
                     amount_deviation
                FROM stats
               WHERE row_number BETWEEN 10 AND 30
            ORDER BY row_number ASC
        """,
            {
                "today": today,
                "order_ids": draft_orders.ids,
            },
        )
        result = {order: vals for order, *vals in self.env.cr.fetchall()}
        for order in draft_orders:
            order_date = order.date_order.date() if order.date_order else today
            (
                last_order_date,
                date_diff_mean,
                date_diff_deviation,
                amount_mean,
                amount_deviation,
            ) = result.get(
                order._origin.id,
                (
                    order_date,
                    0,
                    10000000000,
                    0,
                    10000000000,
                ),
            )
            if date_diff_mean > 25:
                # Correct for varying days per month and leap years.
                date_diff_deviation += 1
            wiggle_room_date = 2 * date_diff_deviation
            order.abnormal_date_warning = (
                not (
                    (order_date - last_order_date).days
                    >= int(date_diff_mean - wiggle_room_date)
                )
            ) and _(
                "The purchasing frequency for %(partner_name)s "
                "appears unusual. Based on your historical data, "
                "the expected next purchase order date is not before "
                "%(expected_date)s (every %(mean)s (± %(wiggle)s) days).\n"
                "Please verify if this date is accurate.",
                partner_name=order.partner_id.display_name,
                expected_date=format_date(
                    self.env,
                    fields.Date.add(
                        last_order_date,
                        days=int(date_diff_mean - wiggle_room_date),
                    ),
                ),
                mean=int(date_diff_mean),
                wiggle=int(wiggle_room_date),
            )
            wiggle_room_amount = 2 * amount_deviation
            order.abnormal_amount_warning = (
                not (
                    amount_mean - wiggle_room_amount
                    <= order.amount_total
                    <= amount_mean + wiggle_room_amount
                )
            ) and _(
                "The amount for %(partner_name)s appears unusual. "
                "Based on your historical data, the expected amount "
                "is %(mean)s (± %(wiggle)s).\n"
                "Please verify if this amount is accurate.",
                partner_name=order.partner_id.display_name,
                mean=order.currency_id.format(amount_mean),
                wiggle=order.currency_id.format(wiggle_room_amount),
            )
