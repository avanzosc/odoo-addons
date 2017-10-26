# -*- coding: utf-8 -*-
# Copytight 2017 Ainara Galdona - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, exceptions, models

TYPE2MSGFIELD = {
    'sale_warn': 'sale_warn_msg',
    'purchase_warn': 'purchase_warn_msg',
    'picking_warn': 'picking_warn_msg',
    'invoice_warn': 'invoice_warn_msg',
}

TYPE2MSGTEXT = {
    'sale_warn': 'Sale Creation Warning:',
    'purchase_warn': 'Purchase Creation Warning:',
    'picking_warn': 'Picking Creation Warning:',
    'invoice_warn': 'Invoice Creation Warning:',
}


class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.multi
    def _get_warning_message(self, type):
        self.ensure_one()
        if type not in TYPE2MSGFIELD:
            return ('no-message', False)
        fields = [type, TYPE2MSGFIELD.get(type)]
        record = self.read(fields)[0]
        return (record.get(type), record.get(TYPE2MSGFIELD.get(type)))

    @api.multi
    def get_partner_warning(self, types, src_object, continue_method):
        self.ensure_one()
        complete_msg = ''
        warn_types = []
        for type in types:
            if type not in TYPE2MSGTEXT:
                continue
            warn, msg = self._get_warning_message(type=type)
            warn_types += [warn]
            complete_msg += u'/n{}/n{}/n'.format(TYPE2MSGTEXT.get(type), msg)
        origin_reference = u'{},{}'.format(src_object._model, src_object.id)
        if 'block' in warn_types:
            blocking_msg = u'{}/n{}'.format(
                _("Some warning doesn't allow to continue this process."),
                complete_msg)
            raise exceptions.Warning(blocking_msg)
        elif 'warning' in warn_types:
            return self.env['partner.show.warning.wiz'].create({
                'exception_msg': complete_msg,
                'partner_id': self.id,
                'origin_reference': origin_reference,
                'continue_method': continue_method,
                }).action_show()
        else:
            return getattr(src_object.with_context(
                bypass_warning=True), u'{}'.format(continue_method))()
