# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from markupsafe import Markup

from odoo import _, api, models
from odoo.tools import format_amount, format_date


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    _history_fields = {
        "applied_on",
        "categ_id",
        "product_tmpl_id",
        "product_id",
        "compute_price",
        "fixed_price",
        "percent_price",
        "base",
        "base_pricelist_id",
        "price_discount",
        "price_round",
        "price_surcharge",
        "price_min_margin",
        "price_max_margin",
        "min_quantity",
        "date_start",
        "date_end",
    }

    def _get_history_target(self):
        self.ensure_one()

        if self.product_id:
            return self.product_id.display_name

        if self.product_tmpl_id:
            return self.product_tmpl_id.display_name

        if self.categ_id:
            return _("Category: %s") % self.categ_id.display_name

        return _("All products")

    def _get_history_base(self):
        self.ensure_one()

        if self.base == "pricelist" and self.base_pricelist_id:
            return self.base_pricelist_id.display_name

        selection = dict(self._fields["base"]._description_selection(self.env))
        return selection.get(self.base, self.base or "")

    def _get_history_price(self):
        self.ensure_one()

        if self.compute_price == "fixed":
            amount = format_amount(
                self.env,
                self.fixed_price,
                self.currency_id,
            )
            return _("Fixed price: %s") % amount

        if self.compute_price == "percentage":
            return _("%s %% of discount") % (f"{self.percent_price:g}")

        surcharge = format_amount(
            self.env,
            self.price_surcharge,
            self.currency_id,
        )
        minimum_margin = format_amount(
            self.env,
            self.price_min_margin,
            self.currency_id,
        )
        maximum_margin = format_amount(
            self.env,
            self.price_max_margin,
            self.currency_id,
        )

        return _(
            "Formula for %(base)s: "
            "discount %(discount)s %%, "
            "rounding %(rounding)s, "
            "surcharge %(surcharge)s, "
            "minimum margin %(minimum)s y "
            "maximum margin %(maximum)s"
        ) % {
            "base": self._get_history_base(),
            "discount": f"{self.price_discount:g}",
            "rounding": f"{self.price_round:g}",
            "surcharge": surcharge,
            "minimum": minimum_margin,
            "maximum": maximum_margin,
        }

    def _get_history_snapshot(self):
        self.ensure_one()

        return {
            "target": self._get_history_target(),
            "price": self._get_history_price(),
            "min_quantity": f"{self.min_quantity:g}",
            "date_start": (
                format_date(self.env, self.date_start) if self.date_start else ""
            ),
            "date_end": (format_date(self.env, self.date_end) if self.date_end else ""),
        }

    def _get_history_labels(self):
        return {
            "target": _("Applies to"),
            "price": _("Price condition"),
            "min_quantity": _("Minimum quantity"),
            "date_start": _("Start date"),
            "date_end": _("End date"),
        }

    def _post_pricelist_history(
        self,
        title,
        changes,
    ):
        self.ensure_one()

        if not self.pricelist_id or not changes:
            return

        items = Markup("").join(
            Markup("<li><strong>{}</strong>: {}</li>").format(label, value)
            for label, value in changes
        )

        body = Markup("<p><strong>{}</strong></p><ul>{}</ul>").format(title, items)

        self.pricelist_id.message_post(
            body=body,
            subtype_xmlid="mail.mt_note",
        )

    def _post_created_history(self):
        self.ensure_one()

        snapshot = self._get_history_snapshot()
        labels = self._get_history_labels()

        changes = [
            (labels["target"], snapshot["target"]),
            (labels["price"], snapshot["price"]),
        ]

        if self.min_quantity:
            changes.append(
                (
                    labels["min_quantity"],
                    snapshot["min_quantity"],
                )
            )

        if self.date_start:
            changes.append(
                (
                    labels["date_start"],
                    snapshot["date_start"],
                )
            )

        if self.date_end:
            changes.append(
                (
                    labels["date_end"],
                    snapshot["date_end"],
                )
            )

        self._post_pricelist_history(
            _("New pricelist line"),
            changes,
        )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        if self.env.context.get("skip_pricelist_item_history"):
            return records

        for record in records:
            record._post_created_history()

        return records

    def write(self, vals):
        if self.env.context.get(
            "skip_pricelist_item_history"
        ) or not self._history_fields.intersection(vals):
            return super().write(vals)

        snapshots_before = {
            record.id: record._get_history_snapshot() for record in self
        }

        result = super().write(vals)

        labels = self._get_history_labels()

        for record in self:
            before = snapshots_before[record.id]
            after = record._get_history_snapshot()

            detail_changes = []

            for key, label in labels.items():
                old_value = before[key] or _("Without value")
                new_value = after[key] or _("Without value")

                if old_value == new_value:
                    continue

                value = Markup("{} → {}").format(
                    old_value,
                    new_value,
                )

                detail_changes.append((label, value))

            # No publicamos nada si realmente no hay cambios
            if not detail_changes:
                continue

            # La línea afectada se muestra SIEMPRE,
            # aunque el producto/categoría no haya cambiado.
            changes = [
                (_("Affected line"), after["target"]),
            ]

            changes.extend(detail_changes)

            record._post_pricelist_history(
                _("Modified pricelist line"),
                changes,
            )

        return result

    def unlink(self):
        if self.env.context.get("skip_pricelist_item_history"):
            return super().unlink()

        for record in self:
            snapshot = record._get_history_snapshot()
            record._post_pricelist_history(
                _("Deleted pricelist line"),
                [
                    (
                        _("Product"),
                        snapshot["target"],
                    ),
                    (
                        _("Price condition"),
                        snapshot["price"],
                    ),
                ],
            )

        return super().unlink()
