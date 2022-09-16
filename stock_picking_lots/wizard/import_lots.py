# Copyright (C) 2013 Obertix Free Software Solutions (<http://obertix.net>).
#                    cubells <info@obertix.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields,  models
import xlrd
import base64


def convert2str(value):
    new_value = str(value).strip()
    if "." in new_value:
        new_value = new_value[:new_value.index(".")]
    return new_value


class ImportInventory(models.TransientModel):
    _name = "import.lots"
    _description = "Import lots"

    data = fields.Binary(
        string="File",
        required=True,
    )
    name = fields.Char(
        string="Filename",
    )

    @api.multi
    def action_import(self):
        self.ensure_one()
        picking_obj = self.env["stock.picking"]
        product_obj = self.env["product.product"]
        lot_obj = self.env["stock.production.lot"]
        quant_obj = self.env["stock.quant"]
        picking = picking_obj.browse(self.env.context["active_id"])
        file_1 = base64.decodestring(self.data)
        book = xlrd.open_workbook(file_contents=file_1)
        sheet = book.sheet_by_index(0)
        error_logs = []
        for counter in range(sheet.nrows):
            line_error_log = []
            rowValues = sheet.row_values(counter, 0, end_colx=sheet.ncols)
            try:
                default_code = convert2str(rowValues[0])
                if default_code.upper() == "REFERENCIA":
                    continue
                lotname = convert2str(rowValues[1])
                variant = convert2str(rowValues[2])
                locationname = ""
                imeiname = ""
                lotref = ""
                if len(rowValues) > 3:
                    locationname = convert2str(rowValues[3])
                if len(rowValues) > 4:
                    imeiname = convert2str(rowValues[4])
                if len(rowValues) > 5:
                    lotref = convert2str(rowValues[5])
                if not lotname:
                    error_logs.append(_("Line {}:\n* Lot Name is not included.").format(
                        counter + 1))
                    continue
            except Exception:
                raise exceptions.Warning(
                    _("The file has not a valid format: REFERENCE, "
                      "SERIAL NUMBER, VARIANT"))
            dest_location = False
            if locationname:
                locationobj = self.env["stock.location"]
                location = locationobj.search([
                    ("complete_name", "ilike", locationname),
                ])
                if not location:
                    line_error_log.append(_(
                        "* Location does not exists: {}.").format(locationname))
                for loc in location:
                    l_name = loc.name_get()[-1][1]
                    if l_name == locationname:
                        dest_location = loc
                        break
                if not dest_location:
                    line_error_log.append(_(
                        "* Location not found: {}//{}.").format(locationname, l_name))
            product = product_obj.search([
                ("default_code", "=", default_code),
                ("attribute_value_ids", "=", variant)])
            if not product:
                line_error_log.append(
                    _("* Product not found."))
            elif len(product) > 1:
                line_error_log.append(
                    _("* There is more than one product with code [{}].").format(
                        default_code))
            else:
                moves = picking.move_lines.filtered(
                    lambda m: m.has_tracking != "none" and
                    m.product_id == product)
                if not moves:
                    line_error_log.append(
                        _("* The product with code [{}] is not in the picking.").format(
                            default_code))
                for move in moves:
                    if dest_location:
                        move.location_dest_id = dest_location
                    prodlot = lot_obj.search([
                        ("name", "=", lotname),
                        ("product_id", "=", product.id)])
                    if picking.picking_type_id.use_create_lots:
                        if prodlot:
                            line_error_log.append(
                                _("* Lot {} already exists.").format(lotname))
                        if picking.move_line_ids.filtered(
                                lambda line: line.lot_name == lotname and
                                line.product_id == product):
                            line_error_log.append(
                                _("* Lot {} already selected.").format(lotname))
                            continue
                        product_lines = move.move_line_ids.filtered(
                            lambda line: not line.lot_name and not line.lot_id)
                        if product_lines and not prodlot:
                            product_lines[:1].write({
                                "lot_name": lotname,
                                "lot_ref": lotref,
                                "imei": imeiname,
                                "location_dest_id": move.location_dest_id.id,
                                "qty_done": 1.0,
                            })
                    if picking.picking_type_id.use_existing_lots:
                        if move.state == "assigned":
                            move._do_unreserve()
                        if move.reserved_availability == move.product_qty:
                            continue
                        if not prodlot:
                            line_error_log.append(
                                _("* Lot {} not found.").format(lotname))
                        else:
                            available_qty = quant_obj._get_available_quantity(
                                product, move.location_id, lot_id=prodlot)
                            if not available_qty:
                                line_error_log.append(
                                    _("* Lot {} is not available.").format(lotname))
                            else:
                                if not prodlot.imei:
                                    prodlot.imei = imeiname
                                if not prodlot.ref:
                                    prodlot.ref = lotref
                        move._update_reserved_quantity(
                            1.0, move.product_qty,
                            move.location_id, lot_id=prodlot)
            if line_error_log:
                error_logs.append(_("Line {}:\n{}").format(
                    counter + 1, "\n".join(line_error_log)))
        picking.write({
            "import_lot_error_log": "\n".join(error_logs) if error_logs else "",
        })
        picking.action_assign()
        return True
