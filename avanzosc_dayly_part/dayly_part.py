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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from osv import osv
from osv import fields

class dayly_part(osv.osv):

    _name = 'dayly.part'
    _description = 'Farm Dayly Part'
 
    _columns = {
            'location_id': fields.many2one('stock.location', 'Location', domain=[('usage', '=', 'internal')]),
            'date': fields.date('Date'),
            'prodlot_id': fields.many2one('stock.production.lot', 'Lot'),
            'eggs_weigth': fields.float('Eggs weigth'),
            'lecture_date': fields.date('Lecture Date'),
            'water_lecture': fields.float('Water Lecture'),
            'water_consum': fields.float('Water Consumtion'),
            'water_price': fields.float('Water Price'),
            'max_temp': fields.float('Max. Temperature'),
            'min_temp': fields.float('Min. Temperature'),
    }
    
    
    def onchange_lecture(self, cr, uid, ids, lot, water_lec, part_date, context=None):
        val={}
        date = False
        part = False
        if lot and water_lec:
            dayly_obj = self.pool.get('dayly.part')
            dayly_list=dayly_obj.search(cr,uid,[('prodlot_id', '=', lot), ('lecture_date','<', part_date)])
            if dayly_list:
                for dayly_id in dayly_list:
                    dayly_o = dayly_obj.browse(cr,uid,dayly_id)
                    if dayly_o.lecture_date > date:
                        part = dayly_o
                        date = dayly_o.lecture_date        
                date_diff =relativedelta(datetime.strptime(part_date,"%Y-%m-%d"), datetime.strptime(date,"%Y-%m-%d")).days
                if date_diff > 0:
                    cons = water_lec - part.water_lecture
                    cons = cons / date_diff
                val = {'water_consum':cons}
        return {'value':val}
dayly_part()