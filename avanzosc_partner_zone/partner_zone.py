# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2011 - 2012 Avanzosc <http://www.avanzosc.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv, fields
from tools.translate import _

class partner_zone(osv.osv):    
    _name = 'partner.zone'
    _description = 'Zone Master for the partner'
    
    _columns = {
        'code': fields.char('Code', size=64, required=True),
        'name': fields.char('Name', size=64, required=True),
        'analytic_acc': fields.many2one('account.analytic.account', 'Analytic account', required=True),
        
    }
partner_zone()

class res_partner_address(osv.osv):
    _inherit = 'res.partner.address' 
    
    _columns = {
        'zone_id': fields.many2one('partner.zone', 'Zone'),
        'analytic': fields.many2one('account.analytic.account', 'Analytic account'),
    }

    def onchange_zone(self, cr, uid, ids, zone_id, zip, context=None):
        res = {}
        account_obj = self.pool.get('account.analytic.account')
        zone_obj = self.pool.get('partner.zone')
        if not ids:
            res = {
                'type': 'other',
                'zone_id': False,
            }
            warning = {
                'title': 'Account Error',
                'message': 'Cannot create an account! Please, save this address first!',
            }
        if not zone_id:
            return res
        for address in self.browse(cr, uid, ids):
            if not zip:
                raise osv.except_osv(_('Error!'),_('Zip does not exist!!\nPlease, fill the zip first.'))
            zone = zone_obj.browse(cr, uid, zone_id)
            if not address.partner_id.property_product_pricelist:
                raise osv.except_osv(_('Error!'),_('Partner has no sale pricelist set!'))
            data = {
                'name': zone.name + ' - ' + zip + ' - ' + address.partner_id.name,
                'partner_id': address.partner_id.id,
                'pricelist_id': address.partner_id.property_product_pricelist.id,
                'to_invoice': 1,
                'parent_id': zone.analytic_acc.id,
            }
            if zone_id and not address.analytic:
                id = account_obj.create(cr, uid, data)
                res = {
                    'analytic': id,
                }
                warning = {
                    'title': 'Account Created',
                    'message': 'Account created: ' + data['name']
                }
            elif zone_id and address.analytic:
                account_obj.write(cr, uid, address.analytic.id, data)
                res = {
                    'analytic': address.analytic.id,
                }
                warning = {
                    'title': 'Account Modified',
                    'message': 'Account modified: ' + data['name']
                }
        return {'value': res, 'warning': warning}
    
res_partner_address()