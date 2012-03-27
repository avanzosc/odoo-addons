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
import time, datetime

class crm_opport2subscription(osv.osv_memory):
    """ Make suscription from opportunity """

    _name = "crm.opport2subscription"
    _description = "Make suscription"
    
  #Mira los campos del Wizard y comprueba que ninguno este vacio.  
    def view_init(self, cr, uid, fields, context=None):
        """
        This function raise an error when there is no values for the wizard
        """

        crm_lead_obj = self.pool.get('crm.lead')
        record_id = context and context.get('active_id', False) or False
        lead = crm_lead_obj.browse(cr, uid, record_id, context=context)
        partner = lead.partner_id
        session = lead.session_id
        #session2 = lead.session_id2
        contact = lead.contact_id
        if not(partner)or not(session) or not(contact):
            raise osv.except_osv(_("Warning"), _("Create Fist the Partner,Seesion and Contact"))
    
    #Coge los campos actuales de partner, contact y seasson.
    def default_get(self, cr, uid, fields, context=None):
        """
        This function takes the actual value of:
        partner_id
        contact_id
        seassion_id
        session_id2
        for the wizard.
        """
        record_id = context and context.get('active_id', False) or False
        res = super(crm_opport2subscription, self).default_get(cr, uid, fields, context=context)
        if record_id:    
            crm_lead = self.pool.get('crm.lead').browse(cr, uid, record_id, context=context)
            if 'partner_id' in fields:
                res.update({'partner_id':crm_lead.partner_id.id})
            
            if 'contact_id' in fields:
                res.update({'contact_id':crm_lead.contact_id.id})
              
            if 'session_id' in fields:
                res.update({'session_id': crm_lead.session_id.id})
            
            if 'session_id2' in fields:
                res.update({'session_id2': crm_lead.session_id2.id})
        return res


    def _selectPartner(self, cr, uid, context=None):
        """
        This function gets default value for partner_id field.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        @return: default value of partner_id field.
        """
        if context is None:
            context = {}

        lead_obj = self.pool.get('crm.lead')
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            return False

        lead = lead_obj.read(cr, uid, active_id, ['partner_id'])
        return lead['partner_id']
		
    def _selectCourse(self, cr, uid, context=None):
        """
        This function gets default value for course_id field.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        @return: default value of partner_id field.
        """
        if context is None:
            context = {}

        lead_obj = self.pool.get('crm.lead')
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            return False

        lead = lead_obj.read(cr, uid, active_id, ['course_id'])
        return lead['course_id']

		
    def action_apply(self, cr, uid, ids, context=None):
        """
        This function  create Suscription from oprtunity on given case.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of crm make sales' ids
        @param context: A standard dictionary for contextual values
        @return: Dictionary value of created sales order.
        """
        if context is None:
            context = {}
        #Para coger los activos del crm.lead
        ###############################################
        record_id =context and context.get('active_id' or False) or False 
        ##################################################
        #--------------   
        ##LOS OBJETOS##
        #--------------    
        crm_lead_obj = self.pool.get('crm.lead')
        training_subscription_obj = self.pool.get('training.subscription')
        training_subscription_line_obj = self.pool.get('training.subscription.line')
        res_partner_obj = self.pool.get('res.partner')
        job_obj = self.pool.get('res.partner.job')
        #---------------------------------------
        ##RECOGER OBJ WIZARD##
        #---------------------------------------
        wizard = self.browse(cr, uid, ids[0], context=context)
        partner = wizard.partner_id.id
        session = wizard.session_id.id
        contact = wizard.contact_id.id
        session2 = wizard.session_id2.id
        job = job_obj.search(cr,uid,[('contact_id', '=', contact)])
        if not job:
            job = job_obj.create(cr,uid,{'contact_id':contact},context)
        else: 
            job = job[0]
        #-------------------------------------------
        ##Recogemos el address_id##
        #-------------------------------------------
        lead = crm_lead_obj.browse(cr, uid, record_id)
        #print lead 
        address = lead.partner_address_id.id
        #--------------------------------------------
        ##Recogemos price y PriceList##  
        #----------------------------- -------------- 
        pricelist = res_partner_obj.browse(cr,uid,partner).property_product_pricelist.id
        price = 1.0
            
        valsForm = {
                        'partner_id':partner,
                        'address_id':address,               
        }
        #INSERT Form
        new_training_subscriotion_obj = training_subscription_obj.create(cr,uid,valsForm,context)
        valsLine1 ={
                       'subscription_id':new_training_subscriotion_obj,
                       'job_id': job,
                       'session_id':session,
                       'price_list_id':pricelist,
                       'price': price,
                       
        }
        #INSERT Line
        new_training_subscriotion_line_obj = training_subscription_line_obj.create(cr,uid,valsLine1,context)
        crm_lead_obj.write(cr,uid,record_id,{'subscription_id':new_training_subscriotion_obj})
        if session2 and session != session2:
             valsLine2 ={
                       'subscription_id':new_training_subscriotion_obj,
                       'job_id': job,
                       'session_id':session2,
                       'price_list_id':pricelist,
                       'price': price,
                       
            }
             #INSERT Line
             new_training_subscriotion_line_obj = training_subscription_line_obj.create(cr,uid,valsLine2,context)
        value = {
                    'name':_('Subscription'),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'training.subscription',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'res_id': int(new_training_subscriotion_obj)
        }
        return value
			
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', required=True),
        'contact_id': fields.many2one('res.partner.contact', 'Contact', required=True),
        'session_id':fields.many2one('training.session', 'Session'),
        'session_id2':fields.many2one('training.session', 'Op.Session'),
        
    }
crm_opport2subscription()
