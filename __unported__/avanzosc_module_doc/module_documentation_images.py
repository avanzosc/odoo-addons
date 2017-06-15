# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2013 AvanzOSC S.L. All Rights Reserved
#    Date: 24/07/2013
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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

from openerp.osv import osv, fields
import base64, urllib

class module_extra_documentation_images(osv.osv):
    
    _name = 'module.doc.image'
    
    def get_image(self, cr, uid, id):
        each = self.read(cr, uid, id, ['filename'])
        try:
            (filename, header) = urllib.urlretrieve(each['filename'])
            f = open(filename , 'rb')
            img = base64.encodestring(f.read())
            f.close()
        except:
            img = ''
        return img
    
    def _get_image(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for each in ids:
            res[each] = self.get_image(cr, uid, each)
        return res
    
    _columns = {
        'name':fields.char('Image Title', size=100, required=True),
        'filename':fields.char('File Location', size=250),
        'preview':fields.function(_get_image, type="binary", method=True),
        'doc_id': fields.many2one('module.doc','Extra documentation'),
    }

module_extra_documentation_images()