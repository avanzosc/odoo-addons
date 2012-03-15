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

class website(osv.osv):
 
    _name = 'website'
    _description = 'Website'
 
    _columns = {
            'name':fields.char('Name', size=64),
            'description':fields.text('Description'),
            'traffic':fields.text('Traffic'),
                 
        }
website()


class sale_order_line(osv.osv):
    _inherit ='sale.order.line' 
    
    def onchange_website(self, cr, uid, ids, website, product_id, context=None):
        ''' 
        Distribución analitica --> account.analytic.plan.instance
        Cuenta analitica --> account.analytic.account
        Linea cuenta analitica --> account.analytic.plan.instance_line
        '''
        val ={}
        #######################################
        #Objetos
        #######################################
        account_analytic_plan_instance = self.pool.get('account.analytic.plan.instance')
        #distrubucion_analitica = self.pool.get('account.analytic.plan.instance')
        account_analytic_account = self.pool.get('account.analytic.account')
        #cuenta_analitica = self.pool.get('account.analytic.account')
        account_analytic_plan_instance_line = self.pool.get('account.analytic.plan.instance.line')
        #linea_cuenta_analitica = self.pool.get('account.analytic.plan.instance.line')
        #######################################
        #Warning
        #######################################
        warning={}
        title = False
        message = False
        #######################################
        #Inicializaciones
        #######################################
        kont = 0
        objeto =''
        midistribucion =''
        if website:
            product_name = self.pool.get('product.product').browse(cr, uid, product_id).name or ''
            website = self.pool.get('website').browse(cr, uid, website) or ''
            website_name = website.name
            #miramos antes de concatenar.
            if not website.description:
                descripcion =''
            else:
                descripcion = website.description
            if not website.traffic:
                trafico = ''
            else:
                trafico = website.traffic
                
            if trafico =='' and descripcion=='':
                objeto = ''
            else:
                 if trafico !='' and descripcion =='':
                     objeto = trafico
                 else:
                     if trafico =='' and descripcion !='':
                        objeto = descripcion
                     else:
                        if trafico !='' and descripcion !='':
                            objeto += descripcion +'\n'+trafico+'\n'
            
            res = product_name+'-'+website.name
            notas = objeto
            #print notas
            #1.mirar si exite Dsitribución analitica con ese nombre = <res>.
            exist_account = account_analytic_plan_instance.search(cr,uid,[('name','=',res)])
            if not exist_account:
            #1.Creamos nueva distribución analítica.
                valDisitribucionAnalalitica= {
                      'name':res,
                      'plan_id':1,    
                }
                new_account_analytic_plan_instance = account_analytic_plan_instance.create(cr,uid,valDisitribucionAnalalitica,context)
                midistribucion = new_account_analytic_plan_instance
            else:
                #Asignar valor a midistribucion
                midistribucion = exist_account[0]
                
            val={
             'name':res,
             'notes':notas,
		     'analytics_id':midistribucion
            }
            
            #2.Existe cuenta analitica con el nombre igual al producto
            existe_cuenta_p = account_analytic_account.search(cr,uid,[('name','=',product_name)])
            if existe_cuenta_p:
                #si existe mirar si existe linea para esa cuenta y plan.
                existe_linea = account_analytic_plan_instance_line.search(cr,uid,[('plan_id','=',midistribucion),('analytic_account_id','=',existe_cuenta_p[0])])
                if not existe_linea:
                    valLinea = {
                                'rate':100.0,
                                'analytic_account_id':existe_cuenta_p[0],
                                'plan_id':midistribucion
                                }
                    new_account_analytic_plan_instance_line = account_analytic_plan_instance_line.create(cr,uid,valLinea,context)
                    kont+=1
              
            else:
                #Creamos Cuenta y Linea
                company_obj = self.pool.get('res.company')
                parent_id = company_obj.search(cr, uid, [])[0]
                parent = company_obj.browse(cr,uid,parent_id)
                valCuenta = {
                            'name':product_name,
                            'parent_id':parent.padre_producto.id,
                            }
                new_account_analytic_account = account_analytic_account.create(cr,uid,valCuenta,context)
                valLinea = {
                                'rate':100.0,
                                'analytic_account_id':new_account_analytic_account,
                                'plan_id':midistribucion
                                }
                new_account_analytic_plan_instance_line = account_analytic_plan_instance_line.create(cr,uid,valLinea,context)
                kont+=1                     
            #3.Existe cuenta con nombre igual a website
            existe_cuenta_w = account_analytic_account.search(cr,uid,[('name','=',website_name)])
            if existe_cuenta_w:
                #print "Existe cuenta con nombre website"
                existe_linea = account_analytic_plan_instance_line.search(cr,uid,[('plan_id','=',midistribucion),('analytic_account_id','=',existe_cuenta_w[0])])
                if not existe_linea:
                	valLinea = {
                            	'rate':100.0,
                            	'analytic_account_id':existe_cuenta_w[0],
                            	'plan_id':midistribucion
                            	}
                	new_account_analytic_plan_instance_line = account_analytic_plan_instance_line.create(cr,uid,valLinea,context)
                	kont+=1
                
            else:
                company_obj = self.pool.get('res.company')
                parent_id = company_obj.search(cr, uid, [])[0]
                parent = company_obj.browse(cr,uid,parent_id)
                valCuenta={
                       'name': website_name,
                       'parent_id':parent.padre_website.id, 
                       }
                new_account_analytic_account = account_analytic_account.create(cr,uid,valCuenta,context)
                valLinea = {
                            'rate':100.0,
                            'analytic_account_id':new_account_analytic_account,
                            'plan_id':midistribucion
                            }
                new_account_analytic_plan_instance_line = account_analytic_plan_instance_line.create(cr,uid,valLinea,context)
                kont+=1
  
            #4. Mirar el cont y depende del resultado printamos el warning.        
            if (kont == 2):  
                title = "Mensaje de aviso"
                message = "--Distribucion Analitica--"
                warning = {
                         'title':title,
                         'message': message
                          }
            return { 'value':val,
                     'warning':warning }
    
    _columns= {
        'website': fields.many2one('website','Website'),
        
    }
    
        
sale_order_line()

class res_company(osv.osv):
     _inherit = 'res.company'
     
     _columns = {
        'padre_website': fields.many2one('account.analytic.account','Padre Website'),
        'padre_producto': fields.many2one('account.analytic.account','Padre Producto'),
        }
res_company()


