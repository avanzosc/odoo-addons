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

class invoice_unreconcile(osv.osv_memory):
    
    _name = 'invoice.unreconcile'

    
    def unreconcile_invoices(self, cr, uid, ids, context=None):
        inv_obj = self.pool.get('account.invoice')
        move_obj = self.pool.get('account.move')
        line_obj = self.pool.get('account.move.line')
        invoice_ids =  context.get('active_ids',[])
        inv_ids = inv_obj.browse(cr,uid, invoice_ids)
        if inv_ids:
            for inv in inv_ids:
                move = move_obj.browse(cr, uid, inv.move_id.id)
                for line in move.line_id:
                    if line.reconcile_id:
                        line_obj._remove_move_reconcile(cr, uid, [line.id])
        return {'type': 'ir.actions.act_window.close()'}
    
invoice_unreconcile()