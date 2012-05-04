
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
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

class training_subscription(osv.osv):
 
    _inherit = 'training.subscription'
    _description = 'Subscription'
 
    def action_print_inscription(self, cr, uid, ids, context=None):
        #iker
        """
        Mira las preinscripciones aceptadas y saca los pertinentes documentos.
        """
        res = {}
        val = False
        ##################
        #OBJETOS.
        ###################
        training_subscription_obj = self.pool.get("training.subscription")
        ##############################
        #WIZ.
        ###############################
        for wiz in self.browse(cr,uid,ids,context):
            #print "state= "+wiz.state
            if  wiz.state == 'confirmed':
                print "OK"
                val = True
            else:
                print "KO"
                raise osv.except_osv(_("Warning"), _("Confirm the suscription first"))
                val = False
        return val
training_subscription()