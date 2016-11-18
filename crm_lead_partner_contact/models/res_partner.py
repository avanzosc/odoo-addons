# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, _


class ResPartner(models.Model):

    _inherit = "res.partner"

    @api.multi
    def name_get(self):
        show_also_email = self.env.context.get('show_also_email', False)
        res = super(ResPartner, self.with_context(show_email=not
                                                  show_also_email)).name_get()
        new_res = []
        for line in res:
            record = self.browse(line[0])
            name = line[1]
            if show_also_email and record.email:
                name += u"\n{} {}".format(_('Email:'), record.email)
            if self.env.context.get('show_phones', False):
                if record.phone:
                    name += u"\n{} {}".format(_('Phone:'), record.phone)
                if record.mobile:
                    name += u"\n{} {}".format(_('Mobile:'), record.mobile)
                if record.fax:
                    name += u"\n{} {}".format(_('Fax:'), record.fax)
            new_res.append((record.id, name))
        return new_res
