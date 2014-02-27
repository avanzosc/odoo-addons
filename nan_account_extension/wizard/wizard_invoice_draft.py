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

import wizard
import netsvc
import pooler

def _invoice_draft(self, cr, uid, data, context):
    pool = pooler.get_pool(cr.dbname)

    ids = data['ids']
    pool.get('account.invoice').write(cr, uid, ids, {'state':'draft'})
    wf_service = netsvc.LocalService("workflow")
    for id in ids:
        wf_service.trg_create(uid, 'account.invoice', id, cr)
    return {}

class wizard_invoice_draft(wizard.interface):
    states = {
        'init': {
            'actions': [_invoice_draft],
            'result': {'type':'state', 'state':'end'}
        }
    }
wizard_invoice_draft('account.invoice.state.draft')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

