# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WizAssignShelf(models.TransientModel):
    _name = "wiz.assign.shelf"
    _description = "Wizard for assign shelf"

    partner_id = fields.Many2one(
        string='Employee', comodel_name='res.partner')
    locker_room_ids = fields.Many2many(
        string='Locker rooms', comodel_name='partner.locker.room',
        readonly=True)
    locker_room_id = fields.Many2one(
        string='Locker room', comodel_name='partner.locker.room')

    @api.model
    def default_get(self, fields):
        result = super(WizAssignShelf, self).default_get(fields)
        if self._context.get('active_id'):
            partner = self.env['res.partner'].browse(
                self._context['active_id'])
            result.update({
                'partner_id': partner.id,
                'locker_room_ids':
                [(6, 0, partner.parent_id.locker_room_ids.ids)]})
        return result

    @api.multi
    def button_assign(self):
        shelf_number = False
        minimun = self.locker_room_id.minimum_number
        while minimun <= self.locker_room_id.maximum_number:
            shelves = self.locker_room_id.mapped('shelves_ids').filtered(
                lambda x: x.shelf_number == minimun)
            if shelves:
                d = max(shelves, key=lambda x: x.assigned_date)
                if (d and d.finished_date and
                        d.finished_date < fields.Date.context_today(self)):
                    shelf_number = d.shelf_number
                    break
            minimun += 1
        if not shelf_number:
            minimun = self.locker_room_id.minimum_number
            while minimun <= self.locker_room_id.maximum_number:
                shelves = self.locker_room_id.mapped('shelves_ids').filtered(
                    lambda x: x.shelf_number == minimun)
                if not shelves:
                    shelf_number = minimun
                    break
                minimun += 1
        if not shelf_number:
            raise ValidationError(
                _('There are no free shelves in selected locker room.'))
        vals = {
            'shelf_number': shelf_number,
            'locker_room_id': self.locker_room_id.id,
            'partner_id': self.partner_id.id,
            'company_id': self.partner_id.parent_id.id,
            'assigned_date': fields.Date.context_today(self)}
        self.env['partner.locker.room.shelf.date'].create(vals)
        return {'type': 'ir.actions.act_window_close'}
