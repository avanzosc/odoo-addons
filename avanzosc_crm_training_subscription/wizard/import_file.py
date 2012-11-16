# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#    Copyright (C) 2012 Avanzosc (http://Avanzosc.com). All Rights Reserved
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
from osv import fields, osv, orm
from tools import ustr
from tools.translate import _
import StringIO
import base64
import csv
import tools
import cStringIO
from collections import defaultdict
import os
import tempfile

try:
    import pyExcelerator as xl
except:
    print 'pyExcelerator Python module not installed'
    
class ucav_import_file(osv.osv_memory):
    
    _name = 'ucav.import.file'
    _description = 'ucav_import_file'
    _columns = {
        'data': fields.binary('File', required=True),
        'name': fields.char('Filename', 256, required=False),
    }
    
    def _convert_to_type(self, chain, to_type):
   
        ret = chain[:]
        if len(ret.strip()) == 0:
            ret = 0
        try:
            ret = to_type(ret)
        except ValueError:
            raise osv.except_osv(_("Error during pricelist import"), _("Value \"%s\" cannot be converted to %s." % (ret, to_type.__name__)))
        return ret
    
    def action_import(self, cr, uid, ids, context=None):
        #################################################
        # ARRAY
        #################################################
        res = {} 
        #################################################
        #################################################
        # OBJETOS
        #################################################
        crm_lead_obj = self.pool.get('crm.lead')
        training_fav_offer_obj = self.pool.get('training.favorite.offer')
        res_country_obj = self.pool.get('res.country')
        res_country_state_obj = self.pool.get('res.country.state')
        #################################################
        try:
            for wiz in self.browse(cr, uid, ids, context):
                if not wiz.data:
                    raise osv.except_osv(_('UserError'), _("You need to select a file!"))
        # Decode the file data
       
            wiz.data.encode('utf8')
            data = base64.b64decode(wiz.data)
            file_type = (wiz.name).split('.')
            input=cStringIO.StringIO(data)
            input.seek(0)
            filename = wiz.name
            reader_info = []
            # Miramos que el fichero sea CSV
            if file_type[1] == "csv":
                reader = csv.reader(input, delimiter=',',lineterminator='\r\n')
            reader_info.extend(reader)
            del reader_info[0]
            keys = []
            values = {}
            keys = [
                    'id','nombre','primerapellido', 'segundoapellido','domicilio','cp','poblacion','provincia',
                    'telefono_fijo','telefono_movil','email','tuenti','facebook','twitter','centro_estudios',
                    'nota_media','ciudadestudios','observaciones','seguimiento','devolucion','lopd',
                    'geconomia','gderecho','gade','gcriminologia','gedinfantil','gedprimariaef','gedprimariaee',
                    'gnutricion','gforestal','gforestalamb','gecoade','gmecanicaamb','gderhumanidades','gagropecuaria',
                    'gmecanica','ginformatica','gambientales','genfermeria','gfisioterapia','gveterinaria',
                    'gcienciasdeporte','gagropecuariaamb','gderade','ginfade','ghumanidades','gpodologia'
                    ]
        
            for i in range(len(reader_info)):
                field = reader_info[i]
                #Diccionario a usar
                values = dict(zip(keys, field))
                country_id = res_country_obj.search(cr,uid,[('code','=','ES')])
                valLead={
                     'name':'OPORTUNIDAD_'+values["id"],
                     'contact_surname': values['primerapellido'],
                     'contact_surname2': values['segundoapellido'],
                     'contact_name': values['nombre'],
                     'type':'opportunity',
                     #'partner_name':,
                     'contact_resum': values['nombre']+' '+values['primerapellido']+' '+values['segundoapellido'],
                     'street': values['domicilio'],
                     'city': values['poblacion'],
                     'zip': values['cp'],
                     'country_id': country_id[0],
                     #'state_id':,
                     'phone': values['telefono_fijo'],
                     'mobile': values['telefono_movil'],
                     'email_from': values['email'],
                     'tuenti': values['tuenti'],
                     'facebook': values['facebook'],
                     'twitter': values['twitter'],
                     'average_mark': values['nota_media'],
                     'description': values['ciudadestudios']+'--'+values['observaciones']+'--'+values['seguimiento']+'--'+values['devolucion']
                     }
            
                new_crm_lead_obj = crm_lead_obj.create(cr,uid,valLead,context)
            
                valFav={}
            #1-->
                if (values['geconomia'] != '-'):
                    valFav = {'sequence': int(values['geconomia']),'offer_name': 'geconomia','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #2-->    
                if (values['gderecho'] != '-'):
                    valFav = {'sequence': int(values['gderecho']),'offer_name': 'gderecho','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #3-->
                if (values['gade'] != '-'):
                    valFav = {'sequence': int(values['gade']),'offer_name': 'gade','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #4-->
                if (values['gcriminologia'] != '-'):
                    valFav = {'sequence': int(values['gcriminologia']),'offer_name': 'gcriminologia','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #5-->    
                if (values['gedinfantil'] != '-'):
                    valFav = {'sequence': int(values['gedinfantil']),'offer_name': 'gedinfantil','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #6-->
                if (values['gedprimariaef'] != '-'):
                    valFav = {'sequence': int(values['gedprimariaef']),'offer_name': 'gedprimariaef','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #7-->    
                if (values['gedprimariaee'] != '-'):
                    valFav = {'sequence': int(values['gedprimariaee']),'offer_name': 'gedprimariaee','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #8-->    
                if (values['gnutricion'] != '-'):
                    valFav = {'sequence': int(values['gnutricion']),'offer_name': 'gnutricion','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #9-->    
                if (values['gforestal'] != '-'):
                    valFav = {'sequence': int(values['gforestal']),'offer_name': 'gforestal','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #10-->    
                if (values['gforestalamb'] != '-'):
                    valFav = {'sequence': int(values['gforestalamb']),'offer_name': 'gforestalamb','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #11-->    
                if (values['gecoade'] != '-'):
                    valFav = {'sequence': int(values['gecoade']),'offer_name': 'gecoade','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #12    
                if (values['gmecanicaamb'] != '-'):
                    valFav = {'sequence': int(values['gmecanicaamb']),'offer_name': 'gmecanicaamb','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #13-->    
                if (values['gderhumanidades'] != '-'):
                    valFav = {'sequence': int(values['gderhumanidades']),'offer_name': 'gderhumanidades','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #14-->    
                if (values['gagropecuaria'] != '-'):
                    valFav = {'sequence': int(values['gagropecuaria']),'offer_name': 'gagropecuaria','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #15-->
                if (values['gmecanica'] != '-'):
                    valFav = {'sequence': int(values['gmecanica']),'offer_name': 'gmecanica','crm_lead_id': new_crm_lead_obj}
                    #intereses.append(valFav)
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #16-->        
                if (values['ginformatica'] != '-'):
                    valFav = {'sequence': int(values['ginformatica']),'offer_name': 'ginformatica','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #17-->
                if (values['gambientales'] != '-'):
                    valFav = {'sequence': int(values['gambientales']),'offer_name': 'gambientales','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #18-->    
                if (values['genfermeria'] != '-'):
                    valFav = {'sequence': int(values['genfermeria']),'offer_name': 'genfermeria','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #19-->
                if (values['gfisioterapia'] != '-'):
                    valFav = {'sequence': int(values['gfisioterapia']),'offer_name': 'gfisioterapia','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #20-->    
                if (values['gveterinaria'] != '-'):
                    valFav = {'sequence': int(values['gveterinaria']),'offer_name': 'gveterinaria','crm_lead_id': new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #21-->
                if (values['gcienciasdeporte'] != '-'):
                    valFav = {'sequence': int(values['gcienciasdeporte']),'offer_name': 'gcienciasdeporte','crm_lead_id':new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #22-->
                if (values['gagropecuariaamb'] != '-'):
                    valFav = {'sequence': int(values['gagropecuariaamb']),'offer_name': 'gagropecuariaamb','crm_lead_id':new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #23-->
                if (values['gderade'] != '-'):
                    valFav = {'sequence': int(values['gderade']),'offer_name': 'gderade','crm_lead_id':new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #24-->    
                if (values['ginfade'] != '-'):
                    valFav = {'sequence': int(values['ginfade']),'offer_name': 'ginfade','crm_lead_id':new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #25-->        
                if (values['ghumanidades'] != '-'):
                    valFav = {'sequence': int(values['ghumanidades']),'offer_name': 'ghumanidades','crm_lead_id':new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
            #26-->    
                if (values['gpodologia'] != '-'):
                    valFav = {'sequence': int(values['gpodologia']),'offer_name': 'gpodologia','crm_lead_id':new_crm_lead_obj}
                    training_fav_offer_obj.create(cr,uid,valFav,context)
                
            return {'type': 'ir.actions.act_window_close'}
        except:
            raise osv.except_osv(_('UserError'), _("You need to select a UTF8 file!"))
            
ucav_import_file()