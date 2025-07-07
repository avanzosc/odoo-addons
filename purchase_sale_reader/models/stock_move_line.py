from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    reader_ps = fields.Char(string="Reader", copy=False)

    picking_type_code = fields.Selection(
        related="picking_id.picking_type_id.code", store=False
    )

    def search_barcode_format(self, model, partner_id, company_id):
        domain = [
            ("model_id.model", "=", model),
            ("partner_ids", "in", [partner_id]),
            "|",
            ("company_id", "=", company_id),
            ("company_id", "=", False),
        ]
        barcode_format = self.env["barcode.format"].search(domain, limit=1)
        return barcode_format

    def search_format_line(self, barcode_format, field_name):
        line = barcode_format.line_ids.filtered(lambda l: l.field_id.name == field_name)
        if not line:
            raise ValidationError(
                _("This format has no line for '%s' field") % field_name
            )
        return line

    def get_lot_field(self):

        picking_type = self.picking_id.picking_type_id

        if picking_type.use_existing_lots:
            return "lot_id"

        elif picking_type.use_create_lots:
            return "lot_name"
        else:
            return None

    @api.onchange("reader_ps")
    def onchange_reader_ps(self):
        if self.reader_ps:

            barcode_format = self.search_barcode_format(
                model=self._name,
                partner_id=self.picking_id.partner_id.id,
                company_id=self.env.company.id,
            )

            if not barcode_format:
                raise ValidationError(
                    _(
                        "No barcode format configured"
                        "for this model and customer was found."
                    )
                )

            product_line = self.search_format_line(barcode_format, "product_id")

            start = product_line.start_pos - 1
            end = product_line.final_pos
            product_code = self.reader_ps[start:end]

            product = self.env["product.product"].search(
                [("default_code", "=", product_code)], limit=1
            )

            if not product:
                product = self.env["product.product"].search(
                    [("barcode", "=", product_code)], limit=1
                )

            if not product:
                product = self.env["product.product"].search(
                    [("product_code", "=", product_code)], limit=1
                )

            if not product:
                raise ValidationError(
                    _("No product with code '%s' was found in Odoo.") % product_code
                )

            self.product_id = product.id

            decode_values = {}
            if barcode_format.type == "variable":
                decode_values = self.env["gs1_barcode"].decode(self.reader_ps)

            if product.tracking != "none":

                lot_field = self.get_lot_field()

                if lot_field:
                    lot_line = self.search_format_line(barcode_format, lot_field)

                    if lot_line and barcode_format.type == "fijo":
                        start = lot_line.start_pos - 1
                        end = lot_line.final_pos
                        lote_code = self.reader_ps[start:end]

                    elif lot_line and barcode_format.type == "variable":
                        lote_code = decode_values.get(lot_line.gs1_barcode_id.ai)

                    if lot_field == "lot_id":
                        lot = self.env["stock.production.lot"].search(
                            [("name", "=", lote_code), ("product_id", "=", product.id)],
                            limit=1,
                        )

                        if not lot:
                            raise ValidationError(
                                _("Lot ‘%s’ was not found for product ‘%s’.")
                                % (lote_code, product.display_name)
                            )

                        self.lot_id = lot.id

                    else:
                        self.lot_name = lote_code

            for line in barcode_format.line_ids:
                field_name = line.field_id.name
                if not field_name or field_name in ["product_id", "lot_id", "lot_name"]:
                    continue

                value = None
                if barcode_format.type == "fijo":
                    start = line.start_pos - 1
                    end = line.final_pos
                    value = self.reader_ps[start:end]
                elif barcode_format.type == "variable":
                    value = decode_values.get(line.gs1_barcode_id.ai)
                if field_name in self._fields and value is not None:
                    field = self._fields[field_name]
                    if field.type == "float":
                        self[field_name] = float(value)
                    elif field.type == "integer":
                        self[field_name] = int(value)
                    else:
                        self[field_name] = value
            weight = decode_values.get("310")
            if weight:
                self.qty_done = round(float(weight), 3)

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if (
                "reader_ps" in values
                and values.get("reader_ps", False)
                and "move_id" in values
                and values.get("move_id", False)
                and "product_id" not in values
            ):
                move = self.env["stock.move"].browse(values.get("move_id", False))
                values["product_id"] = move.product_id.id
        lines = super().create(vals_list)
        return lines
