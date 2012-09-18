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

import time
from copy import copy
from crm import crm
from osv import fields, osv
from tools.translate import _

class training_favorite_offer(osv.osv):
    _name = 'training.favorite.offer'
    _description = 'favorite offer'

    _columns = {
            
        'crm_lead_id': fields.many2one('crm.lead', 'Crm Lead'),
        'offer_id': fields.many2one('training.offer', 'Offer',required=True),
        'sequence': fields.integer('Sequence',required=True),

    }

    
#    _defaults = {
#                 'sequence': lambda self,cr,uid,context={}: self.pool.get('ir.sequence').get(cr, uid, 'training.favorite.offer'),
#                 }
    
training_favorite_offer()

class crm_opportunity(osv.osv):
    _inherit = 'crm.lead'
    
    _columns = {
        'session_id':fields.many2one('training.session', 'Session', domain=[('state', '=', 'opened_confirmed')],required = True),
        'subscription_id': fields.many2one('training.subscription', 'Subscription', readonly = True, domain=[('state', '=', 'opened_confirmed')]),
        'session_id2':fields.many2one('training.session', 'Op.Session', domain=[('state', '=', 'opened_confirmed')]),
        'offer_id':fields.many2one('training.offer','Offer'),
        'favorite_offer1':fields.many2one('training.offer','Favorite Offer 1'),
        'favorite_offer2':fields.many2one('training.offer','Favorite Offer 2'),
        'favorite_offer3':fields.many2one('training.offer','Favorite Offer 3'),
        'favorite_offer4':fields.many2one('training.offer','Favorite Offer 4'),
        'favorite_offer5':fields.many2one('training.offer','Favorite Offer 5'),
        'favorite_offers':fields.one2many('training.favorite.offer','crm_lead_id','Favorite Offers'),
        'offer_ids':fields.many2many('training.offer','offer_opportunity_rel','opportunity_id', 'offer_id', 'Informacion de Offers'),
#        'total_cycle': fields.function(_total_credits, method=True, type='float', string='Total Credits', store=True),

    }


crm_opportunity()

class crm_lead(osv.osv):
    _name='crm.lead'
    _inherit='crm.lead'
    #---------------------------------------------
    #--TRIGGER.--
    #---------------------------------------------
    
    def _check_contact(self,cr,uid,ids):
        #--iker.--
        """ 
        Trigger que mira cuales si el campo del contacto existe.
        Sí no es así, los datos del contact los coge de la pestaña
        de oportunidades.
        """
        for con in self.browse(cr,uid,ids):
            if con.contact_id:
                return True
            else:
                if not con.contact_name and not con.contact_surname:
                    return False
                if not con.contact_name:
                    return False
                if not con.contact_surname:
                    return False
                if not con.contact_surname2:
                    return False
                else:
                    return True
    
    def _check_favorite_offers(self,cr,uid,ids,context=None):
        
        sequences=[]
        offers=[]
        for opportunity in self.browse(cr,uid,ids):
            for favorite_offer in opportunity.favorite_offers:
                sequences.append(favorite_offer.sequence)
                offers.append(favorite_offer.offer_id)
            # -> Xabi 07/2012
            #Verificar que no se repitan las secuencias
            
            examinates=[]
            examinates2=[]
            duplicate=False
            i=0
            while (i<len(sequences) and duplicate==False):
                num=sequences[i]
                offer=offers[i]
                if num in examinates:
                    duplicate==True
                    raise osv.except_osv(_('Error!'),_('There are two favorite offers with the same sequence!'))
                elif offer in examinates2:
                    duplicate==True
                    raise osv.except_osv(_('Error!'),_('There are two favorite offers with the same offer!'))
                else:
                    examinates.append(num)
                    examinates2.append(offer)
                i=i+1
#            #Verificar que las secuencias esten en orden
#            print sequences
#            sorted_seq = copy(sequences)
#            sorted_seq.sort()
#            print sorted_seq
#            if sequences != sorted_seq:
#                raise osv.except_osv(_('Error!'),_('The sequences are not sorted!'))
            # Xabi 07/2012 <-
        return duplicate == False
                        
    #ON CHANGANGE                
    def onchange_contact(self, cr, uid, ids, contact_name,contact_surname,contact_surname2):
        #iker
        """
        Metodo que automaticamnete coge el nombre del contacto en la pestaña
        oportunidades partiendo de un nombre y un apellido. Lo hace
        automaticamnetepartiendo de un punto. 
        """
        value={}
        dev=""
        if  contact_surname:
            dev = dev+" "+contact_surname
        if  contact_surname2:
            dev = dev+" "+contact_surname2
        if contact_name:
            dev = dev+" "+contact_name
        value.update({
                      'contact_resum':dev
        })
        return {
                'value':value
        } 
        
    #ON CHANGANGE    
    def onchange_partner_address_id(self, cr, uid, ids, add, email=False):
        #iker
        if not add:
            return {'value': {'email_from': False, 'country_id': False}}
        address = self.pool.get('res.partner.address').browse(cr, uid, add)
        #OBJETOS
        ################################################################
        res_partner_job_obj = self.pool.get('res.partner.job')
        res_partner_address_obj = self.pool.get('res.partner.address')
        ################################################################
        value={}         
        if address:
            job_list = res_partner_job_obj.search(cr,uid,[('address_id','=',address.id)])
            if job_list :
                job = res_partner_job_obj.browse(cr, uid, job_list[0])     
                contacto = job.contact_id.id 
                value.update({'contact_id':contacto})
        return{'value':value}
                 
    _columns = {
                'contact_name':fields.char('Contact name',size=64),
                'contact_surname':fields.char('Contact surname',size=64),
                'contact_surname2':fields.char('Contact surname2',size=64),
                'contact_resum':fields.char('Contact resum',size=64),
            
    }
    _constraints=[
                 (_check_contact,'Error:contact data is missed',['contact_name','contact_surname','contact_surname2']),
                 (_check_favorite_offers,'Error:There is more than one favorite offer with the same sequence ',['favorite_offers']),
    ]
crm_lead()

class training_offer(osv.osv):
    _inherit = 'training.offer'
    
    _columns = {
                'favorite_offers':fields.one2many('training.favorite.offer','offer_id','Favorite Offers'),
     }
training_offer()           
