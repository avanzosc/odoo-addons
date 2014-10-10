# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv


class wizard_partner_cc_iban(osv.osv_memory):
    _inherit = "wizard.partner.cc.iban"

    def update_cc_iban(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, context=context)[0]
        bank_obj = self.pool.get('res.partner.bank')
        partner_obj = self.pool.get('res.partner')
        partner_ids = context.get('active_ids')
        if partner_ids:
            for partner in partner_obj.browse(cr, uid, partner_ids,
                                              context=context):
                if partner.bank_ids:
                    for bank in partner.bank_ids:
                        new_data = {}
                        country = bank.acc_country_id
                        if not country:
                            country = bank.bank.country
                            new_data['acc_country_id'] = country.id
                        if bank.state == data['bank_state']:
                            continue
                        if bank.state == 'bank':
                            iban = self.convert_to_iban(cr, uid,
                                                        bank.acc_number,
                                                        country.code,
                                                        context=context)
                            exist = bank_obj.search(
                                cr, uid, [('iban', '=', iban),
                                          ('partner_id', '=', partner.id)],
                                context=context)
                            new_data.update(
                                {'iban': iban,
                                 'acc_number': '',
                                 'state': 'iban'})
                        elif bank.state == 'iban':
                            ccc = self.convert_to_ccc(cr, uid, bank.iban,
                                                      context=context)
                            exist = bank_obj.search(
                                cr, uid, [('acc_number', '=', ccc),
                                          ('partner_id', '=', partner.id)],
                                context=context)
                            new_data.update(
                                {'acc_number': ccc,
                                 'iban': '',
                                 'state': 'bank'})
                        if not exist:
                            bank_id = bank_obj.copy(cr, uid, bank.id,
                                                    context=context)
                            bank_obj.write(cr, uid, [bank_id], new_data,
                                           context=context)
        return {'type': 'ir.actions.act_window_close'}

wizard_partner_cc_iban()
