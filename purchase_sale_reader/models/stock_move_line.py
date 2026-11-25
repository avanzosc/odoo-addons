from datetime import datetime

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
        barcode_formats = self.env["barcode.format"].search(domain)
        return barcode_formats

    def search_format_line(self, barcode_format, field_name):
        line = barcode_format.line_ids.filtered(
            lambda line_item: line_item.field_id.name == field_name
        )
        if not line:
            raise ValidationError(
                _("This format has no line for '%s' field") % field_name
            )
        return line

    def get_value_from_line(self, line, reader):
        start = line.start_pos - 1
        end = line.final_pos
        return reader[start:end]

    def get_decimal_value_from_position(self, line, reader):
        if not line.decimal_position:
            return None
        pos = line.decimal_position - 1
        if pos < 0 or pos >= len(reader):
            return None
        value = reader[pos : pos + 1]
        return int(value) if value.isdigit() else None

    def _get_barcode_formats_ps(self):
        barcode_formats = self.search_barcode_format(
            model=self._name,
            partner_id=self.picking_id.partner_id.id,
            company_id=self.env.company.id,
        )

        if not barcode_formats:
            raise ValidationError(
                _(
                    "No barcode format configured"
                    "for this model and customer was found."
                )
            )

        return barcode_formats

    def _prepare_product_temp_fields_ps(self, barcode_format, temp_fields):
        try:
            product_line = self.search_format_line(barcode_format, "product_id")
            product_code = self.get_value_from_line(product_line, self.reader_ps)

            product = self.env["product.product"].search(
                [
                    "|",
                    ("default_code", "=", product_code),
                    ("barcode", "=", product_code),
                ],
                limit=1,
            )

            if not product:
                raise ValidationError(
                    _("No product with code or barcode '%s' was found in Odoo.")
                    % product_code
                )

            temp_fields["product_id"] = product.id

            if product.tracking != "none":
                lot_line = self.search_format_line(barcode_format, "lot_name")
                temp_fields["lot_name"] = self.get_value_from_line(
                    lot_line, self.reader_ps
                )

        except Exception:
            return False

        return True

    def _set_manual_expiration_date_ps(self, field_name, value):
        raw_value = value.strip()
        if raw_value:
            try:
                dt_value = datetime.strptime(raw_value, "%y%m%d")
                dt_value = dt_value.replace(hour=0, minute=0, second=0)
                self[field_name] = dt_value

            except ValueError as err:
                raise ValidationError(
                    _("The date '%s' does not have a valid format.") % raw_value
                ) from err

    def _set_quantity_value_ps(self, line, field_name, value):
        decimals = self.get_decimal_value_from_position(line, self.reader_ps) or 0
        self[field_name] = float(value) / (10**decimals)

    def _set_reader_ps_line_value(self, line):
        field_name = line.field_id.name
        value = self.get_value_from_line(line, self.reader_ps)
        field = self._fields[field_name]

        if field_name == "quantity":
            self._set_quantity_value_ps(line, field_name, value)
        elif field_name == "manual_expiration_date":
            self._set_manual_expiration_date_ps(field_name, value)
        elif field.type == "float":
            self[field_name] = float(value)
        elif field.type == "integer":
            self[field_name] = int(value)
        else:
            self[field_name] = value

    def _process_barcode_format_lines_ps(self, barcode_format):
        for line in barcode_format.line_ids:
            field_name = line.field_id.name
            if not field_name or field_name in ["product_id", "lot_name"]:
                continue

            try:
                self._set_reader_ps_line_value(line)

            except Exception:
                return False

        return True

    def _apply_temp_fields_ps(self, temp_fields):
        for field_name, value in temp_fields.items():
            self[field_name] = value

    def _clear_temp_fields_ps(self, temp_fields):
        for field_name in temp_fields.keys():
            self[field_name] = False

    @api.onchange("reader_ps")
    def onchange_reader_ps(self):
        if not self.reader_ps:
            return

        barcode_formats = self._get_barcode_formats_ps()

        for barcode_format in barcode_formats:
            temp_fields = {}

            success = self._prepare_product_temp_fields_ps(barcode_format, temp_fields)

            if not self._process_barcode_format_lines_ps(barcode_format):
                success = False

            if success:
                self._apply_temp_fields_ps(temp_fields)
                break

            self._clear_temp_fields_ps(temp_fields)

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
