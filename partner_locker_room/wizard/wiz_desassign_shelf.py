# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class WizDesassignShelf(models.TransientModel):
    _name = "wiz.desassign.shelf"
    _description = "Wizard for desassign shelf"

    partner_id = fields.Many2one(
        string='Employee', comodel_name='res.partner')
    desassign_shelf_ids = fields.One2many(
        string='Lines', comodel_name='wiz.desassign.shelf.line',
        inverse_name='wiz_id')

    @api.model
    def default_get(self, fields):
        result = super(WizDesassignShelf, self).default_get(fields)
        if self._context.get('active_id'):
            partner = self.env['res.partner'].browse(
                self._context['active_id'])
            vals = []
            dates = partner.mapped('locker_room_shelf_date_ids').filtered(
                lambda x: not x.finished_date)
            for date in dates:
                line_vals = {'shelf_id': date.id}
                vals.append(line_vals)
            result.update({
                'partner_id': partner.id,
                'desassign_shelf_ids': vals})
        return result

    @api.multi
    def button_deallocate(self):
        for date in self.desassign_shelf_ids:
            date.shelf_id.finished_date = fields.Date.context_today(self)
        return {'type': 'ir.actions.act_window_close'}


class WizDesassignShelfLine(models.TransientModel):
    _name = "wiz.desassign.shelf.line"
    _description = "Desassign shelf lines"

    wiz_id = fields.Many2one(
        string='Wizard', comodel_name='wiz.desassign.shelf')
    shelf_id = fields.Many2one(
        string='Shelf', comodel_name='partner.locker.room.shelf.date')
    company_name = fields.Char(
        string='Company', related='shelf_id.company_id.name')
    shelf_name = fields.Char(
        string='Shelf', related='shelf_id.name')
    assigned_date = fields.Date(
        string='Assigned date', related='shelf_id.assigned_date')
