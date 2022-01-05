# Copyright 2022 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class PortalWizard(models.TransientModel):
    _inherit = 'portal.wizard'

    user_template = fields.Many2one(
        'res.users', string='Template user', domain="[('template', '=', True)]",
        help="Use template user to give internal access rights")

    def action_apply(self):
        if self.user_template:
            self.ensure_one()
            self.user_ids.action_apply_extension(self.user_template)
            res = {'type': 'ir.actions.act_window_close'}
        else:
            res = super(PortalWizard, self).action_apply()
        return res


class PortalWizardUser(models.TransientModel):
    _inherit = 'portal.wizard.user'

    def action_apply_extension(self, template_user):
        for wizard_user in self.sudo().with_context(active_test=False):
            user = wizard_user.partner_id.user_ids[0] if \
                wizard_user.partner_id.user_ids else None
            if not user and self.env.context.get('active_model',
                                                 False) == 'res.partner':
                partner_id = self.env.context.get('active_id')
                if wizard_user.partner_id.email != wizard_user.email:
                    wizard_user.partner_id.write({'email': wizard_user.email})
                template_user.copy({'partner_id': partner_id,
                                    'login': wizard_user.email,
                                    'template': False})
