# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    divide = fields.Integer(string="Divide in", default=1)

    def _get_default_dest_location(self):
        if self.location_dest_id != self.move_id.location_dest_id:
            return self.location_dest_id
        return super()._get_default_dest_location()

    def action_create_package(self, base_prefix=None, seq_number=None):
        self.ensure_one()

        name_packages_by_ref = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("stock.name_packages_by_reference")
        )

        pack_vals = {}
        normalized_prefix = None

        if base_prefix:
            normalized_prefix = base_prefix.strip()
            normalized_prefix = re.sub(r"-\d+$", "", normalized_prefix)
        elif name_packages_by_ref and self.reference:
            normalized_prefix = re.sub(r"[\\/\-]", "", self.reference.strip())
            if re.search(r"\d+-\d{3}$", self.reference):
                normalized_prefix = re.sub(r"(\d+)\d{3}$", r"\1", normalized_prefix)

        if normalized_prefix:
            if self.move_id.production_id:
                next_seq = seq_number or (
                    self.move_id.production_id.packaged_finished_moves + 1
                )
            else:
                domain = [("name", "like", f"{normalized_prefix}-%")]
                existing_packages = self.env["stock.quant.package"].search(domain)
                sequence_numbers = [
                    int(pkg.name.rsplit("-", 1)[1])
                    for pkg in existing_packages
                    if len(pkg.name.rsplit("-", 1)) == 2
                    and pkg.name.rsplit("-", 1)[1].isdigit()
                ]
                if seq_number:
                    next_seq = seq_number
                else:
                    next_seq = max(sequence_numbers, default=0) + 1

            pack_vals["name"] = f"{normalized_prefix}-{next_seq:02}"

        return self.env["stock.quant.package"].create(pack_vals)

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

        base_prefix = self.result_package_id.name if self.result_package_id else None

        if base_prefix:
            domain = [("name", "like", re.sub(r"-\d+$", "", base_prefix) + "-%")]
            existing_packages = self.env["stock.quant.package"].search(domain)
            sequence_numbers = [
                int(pkg.name.rsplit("-", 1)[1])
                for pkg in existing_packages
                if len(pkg.name.rsplit("-", 1)) == 2
                and pkg.name.rsplit("-", 1)[1].isdigit()
            ]
            start_seq = max(sequence_numbers, default=0) + 1
        elif self.move_id.production_id:
            start_seq = self.move_id.production_id.packaged_finished_moves + 1
        else:
            start_seq = 1

        first_qty = qty_quantities.pop(0)
        first_packaging_qty = packaging_qty_quantities.pop(0)
        first_package = self.action_create_package(
            base_prefix=base_prefix, seq_number=start_seq
        )

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

        for i, qty in enumerate(qty_quantities, start=1):
            package_seq = start_seq + i
            package = self.action_create_package(
                base_prefix=base_prefix, seq_number=package_seq
            )
            new_vals = self.copy_data()[0]
            new_vals.update(
                {
                    "qty_done": qty,
                    "reserved_uom_qty": (
                        qty if self.move_id.raw_material_production_id else 0.0
                    ),
                    "product_packaging_qty": packaging_qty_quantities[i - 1],
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
