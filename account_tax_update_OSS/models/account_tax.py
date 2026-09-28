# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import models


class AccountTax(models.Model):
    _inherit = "account.tax"

    def update_account_tax_OSS(self):
        self.ensure_one()

        oss_tag = self.env.ref(
            "l10n_eu_oss.tag_oss",
            raise_if_not_found=False,
        )

        mod303123_tag = (
            self.env["account.account.tag"]
            .with_context(
                active_test=False,
                lang="en_US",
            )
            .search(
                [
                    ("name", "=", "+mod303[123]"),
                    ("country_id", "=", self.env.ref("base.es").id),
                    ("applicability", "=", "taxes"),
                ],
                limit=1,
            )
        )

        if "OSS " in (self.name or ""):
            self.l10n_es_type = "no_sujeto_loc"

            # Reemplaza TODAS las etiquetas de TODAS las líneas de reparto
            # por únicamente oss_tag.
            if oss_tag:
                self.repartition_line_ids.write({"tag_ids": [(6, 0, [oss_tag.id])]})

            # Añade +mod303[123] solamente a la línea BASE de factura.
            if mod303123_tag:
                invoice_base_lines = self.invoice_repartition_line_ids.filtered(
                    lambda line: line.repartition_type == "base"
                )

                invoice_base_lines.write({"tag_ids": [(4, mod303123_tag.id)]})
