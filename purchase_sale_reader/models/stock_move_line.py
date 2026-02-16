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
        line = barcode_format.line_ids.filtered(lambda l: l.field_id.name == field_name)
        if not line:
            raise ValidationError(
                _("This format has no line for '%s' field") % field_name
            )
        return line

    def get_value_from_line(self, line, reader):
        start = line.start_pos - 1
        end = line.final_pos
        return reader[start:end]

    @api.onchange("reader_ps")
    def onchange_reader_ps(self):
        if self.reader_ps:

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
            for barcode_format in barcode_formats:
                temp_fields = {}
                success = True
                try:
                    product_line = self.search_format_line(barcode_format, "product_id")
                    product_code = self.get_value_from_line(
                        product_line, self.reader_ps
                    )
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
                    success = False

                for line in barcode_format.line_ids:
                    field_name = line.field_id.name
                    if not field_name or field_name in ["product_id", "lot_name"]:
                        continue
                    try:
                        value = self.get_value_from_line(line, self.reader_ps)
                        field = self._fields[field_name]

                        if field_name == "qty_done":
                            decimals = getattr(line, "decimals", 0) or 0
                            self[field_name] = float(value) / (10**decimals)
                        elif field_name == "manual_expiration_date":
                            raw_value = value.strip()
                            if raw_value:
                                try:
                                    dt_value = datetime.strptime(raw_value, "%y%m%d")
                                    dt_value = dt_value.replace(
                                        hour=0, minute=0, second=0
                                    )
                                    self[field_name] = dt_value

                                except ValueError:
                                    raise ValidationError(
                                        f"The date '{raw_value}' does not have a valid format."
                                    )

                        elif field.type == "float":
                            self[field_name] = float(value)
                        elif field.type == "integer":
                            self[field_name] = int(value)
                        else:
                            self[field_name] = value

                    except Exception:
                        success = False
                        break

                if success:
                    for f, v in temp_fields.items():
                        self[f] = v
                    break
                else:
                    for f in temp_fields.keys():
                        self[f] = False

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
