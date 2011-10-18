# -*- encoding: utf-8 -*-
##############################################################################
#
#    Avanzosc - Avanced Open Source Consulting
#    Copyright (C) 2010 - 2011 Avanzosc <http://www.avanzosc.com>
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

from osv import osv
from osv import fields


class method(osv.osv):
    _inherit = 'inv.method'
 

    def run_all_filters(self, cr, uid, context={}):
        agr_obj = self.pool.get('inv.agreement')
        aggrs = agr_obj.search(cr,uid,[('state','=','running')])
        for a in aggrs:
            methods = agr_obj.browse(cr,uid,a).service.method_ids
            if methods:
                for m in methods:
                    self._run_filters(cr,uid,[m.id],a,context)
	 	    break
	return 0
method()
