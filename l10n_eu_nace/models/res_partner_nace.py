
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartnerNace(models.Model):
    _name = 'res.partner.nace'
    _order = 'parent_left'
    _parent_order = 'name'
    _parent_store = True
    _description = 'NACE Activity'

    # NACE fields
    level = fields.Integer(
        string='Level',
        required=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )
    generic = fields.Char(
        string='ISIC Rev.4',
    )
    rules = fields.Text(
        translate=True,
        string='Rules',
    )
    central_content = fields.Text(
        translate=True,
        string='Contents',
    )
    limit_content = fields.Text(
        translate=True,
        string='Also contents',
    )
    exclusions = fields.Char(
        translate=True,
        string='Excludes',
    )
    # Parent hierarchy
    parent_id = fields.Many2one(
        comodel_name='res.partner.nace',
        string='Parent NACE Category',
        ondelete='restrict',
        index=True,
    )
    child_ids = fields.One2many(
        comodel_name='res.partner.nace',
        inverse_name='parent_id',
        string='Child NACE Categories',
    )
    parent_left = fields.Integer(
        string='Parent Left',
        index=True,
    )
    parent_right = fields.Integer(
        string='Parent Right',
        index=True,
    )

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_(
                'Error ! You can not create recursive activities.'))
