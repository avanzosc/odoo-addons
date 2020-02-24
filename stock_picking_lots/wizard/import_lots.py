# Copyright (C) 2013 Obertix Free Software Solutions (<http://obertix.net>).
#                    cubells <info@obertix.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields,  models
import xlrd
import base64


class ImportInventory(models.TransientModel):
    _name = 'import.lots'
    _description = 'Import lots'

    data = fields.Binary('File', required=True)
    name = fields.Char('Filename')

    @api.multi
    def action_import(self):
        self.ensure_one()
        picking_obj = self.env['stock.picking']
        product_obj = self.env['product.product']
        lot_obj = self.env['stock.production.lot']
        picking = picking_obj.browse(self.env.context['active_id'])
        file_1 = base64.decodestring(self.data)
        book = xlrd.open_workbook(file_contents=file_1)
        sheet = book.sheet_by_index(0)
        for counter in range(sheet.nrows):
            rowValues = sheet.row_values(counter, 0, end_colx=sheet.ncols)
            try:
                default_code = str(rowValues[0]).strip()
                if '.' in default_code:
                    default_code = default_code[:default_code.index('.')]
                if default_code.upper() == 'REFERENCIA':
                    continue
                lotname = str(rowValues[1]).strip()
                if '.' in lotname:
                    lotname = lotname[:lotname.index('.')]
                variant = str(rowValues[2]).strip()
                locationname = ""
                imeiname = ""
                if len(rowValues) > 3:
                    locationname = str(rowValues[3]).strip()
                if len(rowValues) > 4:
                    imeiname = str(rowValues[4]).strip()
            except Exception:
                raise exceptions.Warning(
                    _('The file has not a valid format: REFERENCE, '
                      'SERIAL NUMBER, VARIANT'))
            dest_location = False
            if locationname:
                locationobj = self.env['stock.location']
                location = locationobj.search([
                    ('complete_name', 'ilike', locationname),
                ])
                if not location:
                    raise exceptions.Warning(
                        _("Location does not exists: {}.").format(
                            locationname))
                for l in location:
                    l_name = l.name_get()[-1][1]
                    if l_name == locationname:
                        dest_location = l
                        break
                if not dest_location:
                    raise exceptions.Warning(_(
                        "Location not found: {}//{}").format(
                        locationname, l_name))
            product = product_obj.search([
                ('default_code', '=', default_code),
                ('attribute_value_ids', '=', variant)])
            if len(product) > 1:
                raise exceptions.Warning(
                    _('There is more than one product with code [%s]'
                      % default_code))
            if product:
                moves = picking.move_lines.filtered(
                    lambda m: m.has_tracking != 'none' and
                    m.product_id == product)
                for move in moves:
                    if dest_location:
                         move.location_dest_id = dest_location
                    if picking.picking_type_id.use_create_lots:
                        product_lines = move.move_line_ids.filtered(
                            lambda l: not l.lot_name and not l.lot_id)
                        if product_lines:
                            product_lines[:1].write({
                                'lot_name': lotname,
                                'imei': imeiname,
                                'location_dest_id': move.location_dest_id.id,
                            })
                    if picking.picking_type_id.use_existing_lots:
                        if move.reserved_availability == move.product_qty:
                            continue
                        if move.state == 'assigned':
                            move._do_unreserve()
                        prodlot = lot_obj.search([
                            ('name', '=', lotname),
                            ('product_id', '=', product.id)])
                        if not prodlot:
                            prodlot = lot_obj.create({
                                'product_id': product.id,
                                'name': lotname,
                                'imei': imeiname,
                            })
                        elif not prodlot.imei:
                            prodlot.imei = imeiname
                        move._update_reserved_quantity(
                            1.0, move.product_qty,
                            move.location_id, lot_id=prodlot)
        picking.action_assign()
        return True
