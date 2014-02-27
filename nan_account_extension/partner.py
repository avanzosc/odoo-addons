# -*- encoding: latin-1 -*-
##############################################################################
#
# Copyright (c) 2010 NaN Projectes de Programari Lliure, S.L. All Rights Reserved.
#                    http://www.NaN-tic.com
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import osv
from osv import fields
from tools.translate import _

class res_partner(osv.osv):
    _inherit = 'res.partner'

    def update_account(self, cr, uid, partner_id, account_type, context, force_checked=None):
            
        if account_type not in ('receivable', 'payable'):
            return

        company = self.pool.get('res.users').browse(cr, uid, uid, context).company_id
        parent_account = getattr(company, 'parent_%s_account_id' % account_type )
        if not parent_account:
            return

        partner = self.browse(cr, uid, partner_id, context)
        if account_type == 'receivable':
            checked = partner.customer
        else:
            checked = partner.supplier
        partner_account = getattr(partner, 'property_account_%s' % account_type )

        if not force_checked is None:
            checked = force_checked

        if partner_account:
            if checked:
                # If account already exists, just check if we need to update account name.
                if partner_account.name != partner.name:
                    # We will only update account name if no other partner is using the same account.
                    value = 'account.account,%d' % partner_account.id
                    partners = self.pool.get('ir.property').search(cr, uid, [('value_reference','=',value)], context=context)
                    if len(partners) == 1:
                        self.pool.get('account.account').write(cr, uid, [partner_account.id], {
                            'name': partner.name,
                        }, context)
                return
            
            # If it's not possible to unlink the account we will rollback this change
            # so the property remains the same. Note that we cannot try to unlink first, 
            # because in this case it would always fail because of the fact that it's set
            # as the account in the partner.
            cr.execute('SAVEPOINT remove_account')
            self.write(cr, uid, [partner_id], {
                'property_account_%s' % account_type : False,
            }, context)
            try:
                # Unlink may raise an exception if the account is already set in another partner
                # or if it has account moves.
                self.pool.get('account.account').unlink(cr, uid, [partner_account.id], context)
            except osv.except_osv:
                cr.execute('ROLLBACK TO SAVEPOINT remove_account')
                return

            cr.execute('RELEASE SAVEPOINT remove_account')
            return 

        if not checked:
            return

        partner_ref = partner.ref or ''
        digits = company.account_digits or 0
        code = parent_account.code + '0'*(digits - len(parent_account.code + partner_ref)) + partner_ref

        account_id = self.pool.get('account.account').search(cr, uid, [('code','=',code)], context=context)
        if account_id:
            account_id = account_id[0]
        else:
            account_id = self.pool.get('account.account').create(cr, uid, {
                'name': partner.name,
                'code': code,
                'parent_id': parent_account.id,
                'user_type': parent_account.user_type.id,
                'reconcile': True,
                'type': account_type,
            }, context)
        self.write(cr, uid, [partner_id], {
            'property_account_%s' % account_type : account_id,
        }, context)


    def create(self, cr, uid, vals, context=None):
        id = super(res_partner, self).create(cr, uid, vals, context)
        self.update_account(cr, uid, id, 'receivable', context)
        self.update_account(cr, uid, id, 'payable', context)
        return id

    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids,int) or isinstance(ids,long):
            ids = [ids]
        result = super(res_partner, self).write(cr, uid, ids, vals, context)
        if 'customer' in vals or 'name' in vals:
            for id in ids:
                self.update_account(cr, uid, id, 'receivable', context)
        if 'supplier' in vals or 'name' in vals:
            for id in ids:
                self.update_account(cr, uid, id, 'payable', context)
        return result

    def unlink(self, cr, uid, ids, context=None):
        for id in ids:
            self.update_account(cr, uid, id, 'receivable', context, force_checked = False)
            self.update_account(cr, uid, id, 'payable', context, force_checked = False)
        return super(res_partner, self).unlink(cr, uid, ids, context)


res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

