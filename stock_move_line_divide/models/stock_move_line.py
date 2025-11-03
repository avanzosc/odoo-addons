# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    divide = fields.Integer(string="Divide in", default=1)

    def _get_default_dest_location(self):
        if self.location_dest_id != self.move_id.location_dest_id:
            return self.location_dest_id
        return super()._get_default_dest_location()

    def action_create_package(self, base_prefix=None):
        self.ensure_one()
        name_packages = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("stock.name_packages_by_reference")
        )
        pack_vals = {}

        prefix = None
        if base_prefix:
            prefix = base_prefix.strip()
        elif name_packages and self.reference:
            prefix = self.reference.strip()

        if prefix:
            domain = [("name", "like", prefix + " -%")]
            existing_packages = self.env["stock.quant.package"].search(domain)
            sequence_numbers = []
            for pkg in existing_packages:
                parts = pkg.name.rsplit(" - ", 1)
                if len(parts) == 2 and parts[1].isdigit():
                    sequence_numbers.append(int(parts[1]))
            next_seq = max(sequence_numbers) + 1 if sequence_numbers else 1
            name = f"{prefix} - {next_seq:03}"
            pack_vals.update({"name": name})

        package = self.env["stock.quant.package"].create(pack_vals)
        return package

    def action_divide(self):
        self.ensure_one()

        if self.divide == 0 or self.qty_done == 0:
            raise ValidationError(
                _("The dividing amount or done quantity can not be 0.")
            )

        divide = self.divide
        qty = self.qty_done or self.reserved_uom_qty
        packaging_qty = self.product_packaging_qty

        if self.product_uom_id.is_unit:
            base_qty = qty // divide
            rest = qty % divide
            qty_quantities = [base_qty] * divide

            base_pack_qty = packaging_qty // divide
            packaging_qty_quantities = [base_pack_qty] * divide

            for i in range(int(rest)):
                qty_quantities[i] += 1
                if packaging_qty_quantities[i] != 0:
                    packaging_qty_quantities[i] += 1
        else:
            base_qty = round(qty / divide, 2)
            qty_quantities = [base_qty] * divide
            qty_quantities[-1] = round(qty - sum(qty_quantities[:-1]), 2)

            base_pack_qty = round(packaging_qty / divide, 2)
            packaging_qty_quantities = [base_pack_qty] * divide
            packaging_qty_quantities[-1] = round(
                packaging_qty - sum(packaging_qty_quantities[:-1]), 2
            )

        base_prefix = (
            self.result_package_id.name if self.result_package_id else self.reference
        )

        first_qty = qty_quantities.pop(0)
        first_packaging_qty = packaging_qty_quantities.pop(0)
        first_package = self.action_create_package(base_prefix=base_prefix)

        self.write(
            {
                "qty_done": first_qty,
                "reserved_uom_qty": (
                    first_qty if self.move_id.raw_material_production_id else 0.0
                ),
                "result_package_id": first_package.id,
                "product_packaging_qty": first_packaging_qty,
                "divide": 1,
            }
        )

        for i, qty in enumerate(qty_quantities):
            package = self.action_create_package(base_prefix=base_prefix)
            new_vals = self.copy_data()[0]
            new_vals.update(
                {
                    "qty_done": qty,
                    "reserved_uom_qty": (
                        qty if self.move_id.raw_material_production_id else 0.0
                    ),
                    "product_packaging_qty": packaging_qty_quantities[i],
                    "result_package_id": package.id,
                    "divide": 1,
                }
            )
            self.env["stock.move.line"].with_context(from_action_divide=True).create(
                new_vals
            )

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        packaging = self.product_packaging_id
        move = self.move_id

        if packaging and move and packaging.qty and not move.raw_material_production_id:
            base_qty = (
                move.product_uom_qty - move.quantity_done
                if move.quantity_done
                else move.product_uom_qty
            )
            ratio = base_qty / packaging.qty
            self.qty_done = base_qty
            self.product_packaging_qty = ratio
            self.divide = ratio
        else:
            self.product_packaging_qty = 0
            self.qty_done = 1

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self.env.context.get("from_action_divide"):
                continue

            move = self.env["stock.move"].browse(vals.get("move_id"))
            packaging = (
                move.production_id.product_packaging_id if move.production_id else None
            )

            if (
                packaging
                and packaging.qty
                and not move.raw_material_production_id
                and move.product_id == move.production_id.product_id
            ):
                vals["product_packaging_id"] = packaging.id
                base_qty = (
                    move.product_uom_qty - move.quantity_done
                    if move.quantity_done
                    else move.product_uom_qty
                )
                ratio = base_qty / packaging.qty
                vals.update(
                    {
                        "product_packaging_qty": ratio,
                        "divide": ratio,
                        "qty_done": base_qty,
                    }
                )

        return super().create(vals_list)
