# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tools import email_split
from odoo import api, fields, models


def extract_email(email):
    """ extract the email address from a user-friendly email address """
    addresses = email_split(email)
    return addresses[0] if addresses else ''


class CreateUserWizard(models.TransientModel):
    _name = 'create.user.wizard'
    _description = 'Create User Wizard'

    line_ids = fields.One2many(
        comodel_name='create.user.wizard.line', inverse_name='wizard_id',
        string='Users')

    @api.model
    def default_get(self, fields_list):
        res = super(CreateUserWizard, self).default_get(fields_list)
        partner_ids = self.env.context.get('active_ids', [])
        contact_ids = set()
        user_changes = []
        for partner in self.env['res.partner'].sudo().browse(partner_ids):
            contact_partners = partner.child_ids or [partner]
            for contact in contact_partners:
                # make sure that each contact appears at most once in the list
                if contact.id not in contact_ids:
                    contact_ids.add(contact.id)
                    user_changes.append((0, 0, {
                        'partner_id': contact.id,
                        'email': contact.email,
                        'user_id': contact.user_ids[:1].id,
                    }))
        res.update({'line_ids': user_changes})
        return res

    @api.multi
    def action_apply(self):
        self.ensure_one()
        self.line_ids.action_apply()
        return {'type': 'ir.actions.act_window_close'}


class CreateUserWizardLine(models.TransientModel):
    _name = 'create.user.wizard.line'
    _description = 'Create User Wizard Line'

    wizard_id = fields.Many2one(
        comodel_name='create.user.wizard', string='Wizard', required=True,
        ondelete='cascade')
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner', required=True,
        readonly=True, ondelete='cascade')
    email = fields.Char(string='Email')
    user_id = fields.Many2one(comodel_name='res.users', string='Login User')

    @api.multi
    def action_apply(self):
        self.env['res.partner'].check_access_rights('write')
        lines = self.sudo().with_context(active_test=False)
        for line in lines.filtered(lambda l: not l.user_id and l.email):
            # update partner email, if a new one was introduced
            if line.partner_id.email != line.email:
                line.partner_id.write({'email': line.email})
            company_id = (
                line.partner_id.company_id.id or
                self.env['res.company']._company_default_get('res.users').id)
            line.user_id = line.sudo().with_context(
                company_id=company_id)._create_user()

    @api.multi
    def _create_user(self):
        """ create a new user for line.partner_id
            :returns record of res.users
        """
        company_id = self.env.context.get('company_id')
        return self.env['res.users'].with_context(
            no_reset_password=True).create({
                'email': extract_email(self.email),
                'login': extract_email(self.email),
                'partner_id': self.partner_id.id,
                'company_id': company_id,
                'company_ids': [(6, 0, [company_id])],
            })
