 -*- encoding: utf-8 -*-
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

from osv import osv
from osv import fields

class wiz_insert_marks_teachers(osv.osv_memory):
     _name = 'wiz.insert.marks.teachers'
    _description = 'Wizard insert marks teachers'
    
    def insert_marks(self, cr, uid, ids, context={}):
        #OBJETOS
        ##################################################################
        training_record_obj = self.pool.get('training.record')
        ##################################################################
    
    _columns = {
                'teacher':
                'offer': 
                'seances':
                     
        }
wiz_insert_marks_teachers()