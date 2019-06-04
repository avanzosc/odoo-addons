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
        move_line_obj = self.env['stock.move.line']
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
            except Exception:
                raise exceptions.Warning(
                    _('The file has not a valid format: REFERENCE, '
                      'SERIAL NUMBER, VARIANT'))
            product = product_obj.search([
                ('default_code', '=', default_code),
                ('attribute_value_ids', '=', variant)])
            if len(product) > 1:
                raise exceptions.Warning(
                    _('There is more than one product with code [%s]'
                      % default_code))
            if product:
                move = picking.move_lines.filtered(
                    lambda m: m.has_tracking != 'none' and
                    m.product_id == product)
                if move.state == 'assigned':
                    move._do_unreserve()
                prodlot = lot_obj.search([
                    ('name', '=', lotname), ('product_id', '=', product.id)])
                if not prodlot:
                    prodlot = lot_obj.create({
                        'product_id': product.id,
                        'name': lotname,
                        'product_qty': 1.0,
                    })
                move_lines = move_line_obj.search([
                    ('picking_id', '!=', picking.id),
                    ('product_id', '=', product.id),
                    ('lot_id', '=', prodlot.id),
                ])
                other_moves = move_lines.mapped('move_id')
                if other_moves:
                    other_moves._do_unreserve()
                move._update_reserved_quantity(
                    prodlot.product_qty, move.product_qty, move.location_id,
                    lot_id=prodlot)
                move._action_assign()
                if other_moves:
                    other_moves._action_assign()
        return True
