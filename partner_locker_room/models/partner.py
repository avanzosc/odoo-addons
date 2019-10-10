# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    valid_for_locker_room = fields.Boolean(
        string='Valid for have locker rooms',
        compute='_compute_valid_for_locker_room', store=True)
    multiple_shelves = fields.Boolean(
        string='multiple shelves', default=False)
    locker_room_ids = fields.One2many(
        string='Locker rooms', comodel_name='partner.locker.room',
        inverse_name='partner_id')
    locker_room_shelf_date_ids = fields.One2many(
        string='Locker rooms shelves', inverse_name='partner_id',
        comodel_name='partner.locker.room.shelf.date')
    active_locker_room_shelf_date_ids = fields.Many2many(
        string='Employee active shelves',
        comodel_name='partner.locker.room.shelf.date',
        relation='rel_partner_locker_room_shelf_date',
        column1='partner_id', column2='locker_room_shelf_date_id',
        compute='_compute_active_locker_room_shelf_date_ids', store=True)
    company_locker_room_shelf_date_ids = fields.One2many(
        string='Company locker rooms shelves', inverse_name='company_id',
        comodel_name='partner.locker.room.shelf.date')

    @api.depends('company_type', 'parent_id', 'type')
    def _compute_valid_for_locker_room(self):
        for partner in self:
            if ((partner.company_type == 'person' and
                 partner.type == 'delivery' and partner.parent_id) or
                (partner.company_type == 'company' and not
                 partner.parent_id)):
                partner.valid_for_locker_room = True
            else:
                partner.valid_for_locker_room = False

    @api.depends('locker_room_shelf_date_ids',
                 'locker_room_shelf_date_ids.finished_date')
    def _compute_active_locker_room_shelf_date_ids(self):
        for partner in self:
            dates = partner.mapped('locker_room_shelf_date_ids').filtered(
                lambda x: not x.finished_date)
            partner.active_locker_room_shelf_date_ids = [
                (6, 0, dates.ids)]

    @api.multi
    def button_assign_shelf(self):
        self.ensure_one()
        wiz_obj = self.env['wiz.assign.shelf']
        if not self.multiple_shelves:
            dates = self.mapped('locker_room_shelf_date_ids').filtered(
                lambda x: not x.finished_date)
            if dates:
                error = _(u'The employee {}, have assigned the shelf {}, in '
                          'the locker room {}').format(
                              self.name, dates.shelf_number,
                              dates.locker_room_id.name)
                raise ValidationError(error)
        wiz = wiz_obj.with_context({'active_id': self.id,
                                    'active_ids': self.ids,
                                    'active_model': 'res.partner'}).create({})
        context = self.env.context.copy()
        context.update({'active_id': self.id,
                        'active_ids': self.ids,
                        'active_model': 'res.partner'})
        return {
            'name': _('Assign shelf'),
            'type': 'ir.actions.act_window',
            'res_model': 'wiz.assign.shelf',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': wiz.id,
            'target': 'new',
            'context': context}

    @api.multi
    def button_unsubscribe_assigned_shelf(self):
        self.ensure_one()
        wiz_obj = self.env['wiz.desassign.shelf']
        dates = self.mapped('locker_room_shelf_date_ids').filtered(
            lambda x: not x.finished_date)
        if dates and len(dates) > 1:
            wiz = wiz_obj.with_context(
                {'active_id': self.id,
                 'active_ids': self.ids,
                 'active_model': 'res.partner'}).create({})
            context = self.env.context.copy()
            context.update({'active_id': self.id,
                            'active_ids': self.ids,
                            'active_model': 'res.partner'})
            return {
                'name': _('Select shelves to deallocate'),
                'type': 'ir.actions.act_window',
                'res_model': 'wiz.desassign.shelf',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': wiz.id,
                'target': 'new',
                'context': context}
        if dates and len(dates) == 1:
            dates.write({'finished_date': fields.Date.context_today(self)})


class PartnerLockerRoom(models.Model):
    _name = 'partner.locker.room'
    _description = 'Locker room'

    partner_id = fields.Many2one(
        string='Company', comodel_name='res.partner', required=True)
    code = fields.Char(string='Code')
    name = fields.Char(string='Description')
    minimum_number = fields.Integer(string='Minimum number', default=1)
    maximum_number = fields.Integer(string='Maximum number')
    shelves_ids = fields.One2many(
        string='shelves', comodel_name='partner.locker.room.shelf.date',
        inverse_name='locker_room_id')

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id, _(u'{} - [{}] {}').format(
                    record.partner_id.name, record.code, record.name)))
        return result

    @api.constrains('minimum_number', 'maximun_number')
    def _check_date_end_after_date_start(self):
        self_obj = self.env['partner.locker.room.shelf.date']
        for record in self:
            if record.minimum_number < 1:
                raise ValidationError(
                    _('Minimum number must be greater than or equal to 1.'))
            if record.maximum_number < 1:
                raise ValidationError(
                    _('Maximum number must be greater than or equal to 1.'))
            if record.minimum_number > record.maximum_number:
                raise ValidationError(
                    _('Maximum number must be greater than minimum number.'))
            if record.minimum_number > 1:
                cond = [('locker_room_id', '=', record.id),
                        ('shelf_number', '<', record.minimum_number),
                        ('finished_date', '=', False)]
                shelfs = self_obj.search(cond, limit=1)
                if shelfs:
                    error = _(u'There are active shelves with a number less '
                              'than  {}').format(record.minimum_number)
                    raise ValidationError(error)
            if record.maximum_number > 1:
                cond = [('locker_room_id', '=', record.id),
                        ('shelf_number', '>', record.maximum_number),
                        ('finished_date', '=', False)]
                shelfs = self_obj.search(cond, limit=1)
                if shelfs:
                    error = _(u'There are active shelves with a number greater'
                              ' than  {}').format(record.maximum_number)
                    raise ValidationError(error)


class PartnerLockerRoomShelfDate(models.Model):
    _name = 'partner.locker.room.shelf.date'
    _description = 'Shelf dates'
    _order = 'company_id, locker_room_id, shelf_number, assigned_date'

    name = fields.Char(
        string='Shelf', compute='_compute_name', store=True)
    company_id = fields.Many2one(
        string='Company', comodel_name='res.partner')
    locker_room_id = fields.Many2one(
        string='Locker room', comodel_name='partner.locker.room',
        required=True, ondelete='cascade')
    shelf_number = fields.Integer(
        string='Shelf number', required=True, default=1)
    partner_id = fields.Many2one(
        string='Employee', comodel_name='res.partner')
    partner_reference = fields.Char(
        string='Employee reference', related='partner_id.ref', store=True)
    assigned_date = fields.Date(
        string='Assigned date',
        default=lambda self: fields.Date.context_today(self))
    finished_date = fields.Date(string='Finished date')

    @api.depends('locker_room_id', 'shelf_number')
    def _compute_name(self):
        for date in self.filtered(
                lambda c: c.locker_room_id and c.shelf_number):
            name = _(u'[{}] {}-Shelf {}').format(
                date.locker_room_id.code, date.locker_room_id.name,
                date.shelf_number)
            date.name = name

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id and self.partner_id.parent_id:
            self.company_id = self.partner_id.parent_id.id

    @api.constrains('partner_id','shelf_number', 'locker_room_id',
                    'company_id', 'company_id.multipe_shelves')
    def _check_shelf_finished_date(self):
        for record in self.filtered(
                lambda c: not c.finished_date and c.partner_id and
                c.shelf_number and c.locker_room_id and c.company_id):
            cond = [('id', '!=', record.id),
                    ('company_id.multiple_shelves', '=', False),
                    ('shelf_number', '=', record.shelf_number),
                    ('locker_room_id', '=', record.locker_room_id.id),
                    ('finished_date', '=', False)]
            dates = self.search(cond, limit=1)
            if len(dates) > 0:
                error = _(u'The shelf number {}, of the locker room {}, cannot'
                          ' have 2 empty finished dates').format(
                              record.shelf_number, record.locker_room_id.name)
                raise ValidationError(error)
            cond = [('id', '!=', record.id),
                    ('partner_id', '=', record.partner_id.id),
                    ('company_id.multiple_shelves', '=', False),
                    ('shelf_number', '!=', record.shelf_number),
                    ('locker_room_id', '=', record.locker_room_id.id),
                    ('finished_date', '=', False)]
            dates = self.search(cond, limit=1)
            if len(dates) > 0:
                error = _(u'The employee {}, already assigned the shelf '
                          'number {}, in the locker room {}').format(
                              record.partner_id.name, record.shelf_number,
                              dates.locker_room_id.name)
                raise ValidationError(error)
            cond = [('id', '!=', record.id),
                    ('partner_id', '=', record.partner_id.id),
                    ('company_id.multiple_shelves', '=', True),
                    ('shelf_number', '=', record.shelf_number),
                    ('locker_room_id', '=', record.locker_room_id.id),
                    ('finished_date', '=', False)]
            dates = self.search(cond, limit=1)
            if len(dates) > 0:
                error = _(u'The employee {}, already assigned the shelf {}, in'
                          ' the locker room {}').format(
                              record.partner_id.name, dates.shelf_number,
                              dates.locker_room_id.name)
                raise ValidationError(error)
            cond = [('id', '!=', record.id),
                    ('partner_id', '!=', record.partner_id.id),
                    ('shelf_number', '=', record.shelf_number),
                    ('locker_room_id', '=', record.locker_room_id.id),
                    ('finished_date', '=', False)]
            dates = self.search(cond, limit=1)
            if len(dates) > 0:
                error = _(u'The shelf number {}, is already assigned to the '
                          'employee {}, in the locker room {}').format(
                              record.shelf_number, dates.partner_id.name,
                              dates.locker_room_id.name)
                raise ValidationError(error)
            if (record.finished_date and
                    record.finished_date < record.assigned_date):
                raise ValidationError(
                    _(u'Finished date less than assigned date'))
