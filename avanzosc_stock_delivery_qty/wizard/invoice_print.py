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

class invoice_print(osv.osv_memory):
    
    _name = 'invoice.print'

    
    def print_invoices(self, cr, uid, ids, context=None):
        inv_obj = self.pool.get('account.invoice')
        invoice_ids =  context.get('active_ids',[])
        data = {}
        inv_obj.write(cr, uid, invoice_ids, {'printed':True})
        data.update({'ids':invoice_ids,
                     'model':'account.invoice',})
        return { 'type': 'ir.actions.report.xml',
                'report_name': 'Factura VoV',
                'datas': data,}
    
invoice_print()