# -*- encoding: utf-8 -*-
##############################################################################
#
#    AvanzOSC, Avanzed Open Source Consulting 
#    Copyright (C) 2011-2012 Iker Coranti (www.avanzosc.com). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv
from osv import fields

class training_city(osv.osv):
    _name = 'training.city'
    _description = 'Ciudades de España'
    _rec_name='city_name'
    
    _columns = { 
               'city_name': fields.char('City name', size=128),
               'city_code': fields.char('City code', size=128),
               'provincia': fields.many2one('res.country.state','Provincia'),
               }
training_city()