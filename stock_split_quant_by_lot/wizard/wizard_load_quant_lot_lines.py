# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, _, exceptions
import base64
import csv
import cStringIO


class LoadQuantLotLines(models.TransientModel):

    _name = 'load.quant.lot.lines'

    by_text = fields.Boolean(string='By text')
    by_file = fields.Boolean(string='By file')
    file = fields.Binary(string='File')
    lot_numbers = fields.Text(string='Lot numbers')
    delimiter = fields.Char(string='Delimiter', default='\n')
    origin_move_id = fields.Many2one(comodel_name='stock.move',
                                     string='Origin Move')
    origin_quants = fields.Many2many(comodel_name='stock.quant')
    line_ids = fields.One2many(
        comodel_name='load.quant.lot.lines.line', inverse_name='parent_id',
        string='Lines')

    @api.model
    def view_init(self, fields_list):
        if self.env.context.get('active_model') == 'stock.move':
            move_id = self.env.context.get('active_id', False)
            move = self.env['stock.move'].browse(move_id)
            if not move.quant_ids.filtered(lambda x: x.location_id.usage ==
                                           'internal'):
                raise exceptions.Warning(
                    _(u'There is no quant which can be splitted.'))

    @api.model
    def default_get(self, fields):
        res = super(LoadQuantLotLines, self).default_get(fields)
        if self.env.context.get('active_model') == 'stock.move':
            move_id = self.env.context.get('active_id', False)
            move = self.env['stock.move'].browse(move_id)
            res['origin_move_id'] = move_id
            res['origin_quants'] = [(6, 0, move.quant_ids.filtered(
                lambda x: x.location_id.usage == 'internal').ids)]
        return res

    @api.multi
    @api.onchange('by_file')
    def onchange_by_file(self):
        self.ensure_one()
        if self.by_file:
            self.lot_numbers = False
            self.by_text = False
            self.delimiter = ','

    @api.multi
    @api.onchange('by_text')
    def onchange_by_text(self):
        self.ensure_one()
        if self.by_text:
            self.file = False
            self.by_file = False
            self.delimiter = '\n'

    @api.multi
    def load_from_file(self):
        wiz_line_model = self.env['load.quant.lot.lines.line']
        lines = self.env['load.quant.lot.lines.line']
        product = self.origin_quants and self.origin_quants[0].product_id
        data = base64.b64decode(self.file)
        file_input = cStringIO.StringIO(data)
        file_input.seek(0)
        reader_info = []
        delimeter = self.delimiter and str(self.delimiter) or ','
        reader = csv.reader(file_input, delimiter=delimeter,
                            lineterminator='\r\n')
        try:
            reader_info.extend(reader)
        except Exception:
            raise exceptions.Warning(_('Not a valid file!'))
        keys = [x.lower() for x in reader_info[0]]
        if 'lot_name' not in keys:
            raise exceptions.Warning(_("Not 'lot_name' key found"))
        del reader_info[0]
        for i in range(len(reader_info)):
            field = reader_info[i]
            values = dict(zip(keys, field))
            iter_values = values.copy()
            for key in iter_values.keys():
                if key not in ['lot_name', 'qty']:
                    values.pop(key)
            values.update(
                {'parent_id': self.id,
                 'product_id': product.id})
            lines += wiz_line_model.create(values)
        return lines

    @api.multi
    def load_from_text(self):
        lots = self.lot_numbers.split(self.delimiter or '\n')
        wiz_line_model = self.env['load.quant.lot.lines.line']
        lines = self.env['load.quant.lot.lines.line']
        product = self.origin_quants and self.origin_quants[0].product_id
        for lot in lots:
            vals = {
                'parent_id': self.id,
                'product_id': product.id,
                'lot_name': lot,
                'qty': 1
            }
            lines += wiz_line_model.create(vals)
        return lines

    @api.multi
    def create_residual_lines(self):
        wiz_line_model = self.env['load.quant.lot.lines.line']
        lines = self.env['load.quant.lot.lines.line']
        created_lines_qty = sum(self.mapped('line_ids.qty'))
        for quant in self.origin_quants:
            created_lines_qty = max(created_lines_qty, 0)
            if quant.qty >= created_lines_qty:
                vals = {
                    'parent_id': self.id,
                    'product_id': quant.product_id.id,
                    'lot_name': quant.lot_id.name,
                    'qty': (quant.qty - created_lines_qty),
                }
                lines += wiz_line_model.create(vals)
            created_lines_qty -= quant.qty
        return lines

    @api.multi
    def load_lines(self):
        self.ensure_one()
        lines = self.env['load.quant.lot.lines.line']
        if self.by_file:
            lines += self.load_from_file()
        elif self.by_text:
            lines += self.load_from_text()
        lines += self.create_residual_lines()
        self.line_ids = lines
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'load.quant.lot.lines',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    @api.multi
    def create_inventory_header(self, location_id):
        vals = {
            'name': '{}::{}'.format(self.origin_move_id.name,
                                    self.origin_move_id.origin),
            'filter': 'partial',
            'location_id': location_id,
        }
        return self.env['stock.inventory'].create(vals)

    def reasign_quants(self, move, inventory, before_quants):
        inventory_quants = inventory.mapped('move_ids.quant_ids')
        quants = self.env['stock.quant']
        quants += before_quants
        quants += inventory_quants.filtered(
            lambda x: x.location_id.usage == 'internal')
        for quant in quants:
            move.quant_ids = [(4, quant.id)]
        for quant in move.quant_ids:
            if (quant.location_id.usage != 'internal' and quant in
                    inventory_quants):
                move.quant_ids = [(3, quant.id)]

    @api.multi
    def action_validate(self):
        self.ensure_one()
        location_id = self.origin_move_id.location_dest_id.id
        inventory = self.create_inventory_header(location_id)
        inventory.prepare_inventory()
        inventory_line_model = self.env['stock.inventory.line']
        for line in self.line_ids:
            values = {
                'inventory_id': inventory.id,
                'product_id': line.product_id.id,
                'prod_lot_id': line.get_line_lot_id(),
                'location_id': location_id,
                'product_qty': line.qty,
            }
            inventory_line_model.create(values)
        before_quants = self.origin_move_id.quant_ids
        inventory.with_context(
            load_move_relation=self.origin_move_id).action_done()
        self.reasign_quants(self.origin_move_id, inventory, before_quants)
        return {'type': 'ir.actions.act_window_close'}


class LoadQuantLotLinesLine(models.TransientModel):

    _name = 'load.quant.lot.lines.line'

    parent_id = fields.Many2one(comodel_name='load.quant.lot.lines',
                                string='Parent')
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product')
    lot_name = fields.Char(string='Lot')
    qty = fields.Float(string='Quantity', default=1.0)

    @api.multi
    def get_line_lot_id(self):
        self.ensure_one()
        if not self.lot_name:
            return False
        lot_model = self.env['stock.production.lot']
        domain = [('name', '=', self.lot_name),
                  ('product_id', '=', self.product_id.id)]
        lot = lot_model.search(domain, limit=1)
        if lot:
            return lot.id
        return lot_model.create({'name': self.lot_name,
                                 'product_id': self.product_id.id}).id
