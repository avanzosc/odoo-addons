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
import decimal_precision as dp

from osv import osv
from osv import fields

class l10n_es_tesoreria_plantilla(osv.osv):
    _name = 'l10n.es.tesoreria.plantilla'
    _inherit = 'l10n.es.tesoreria.plantilla'
    _columns = {
                'pagos_rece':fields.one2many('l10n.es.tesoreria.pagos.rece.plan','plan_tesoreria_id', 'Cobros Unicos'),
                'pagos_cash':fields.one2many('l10n.es.tesoreria.pagos.cash.plan', 'plan_tesoreria_id', 'Cash-flow Financiero')
                }
l10n_es_tesoreria_plantilla()

class l10n_es_tesoreria_pagos_rece_plan(osv.osv):
    _name = 'l10n.es.tesoreria.pagos.rece.plan'

    _columns = {
                'name': fields.char('Descripción', size=64),
                'fecha': fields.date('Fecha'),
                'diario': fields.many2one('account.journal', 'Diario'),
                'importe': fields.float('Importe', digits_compute=dp.get_precision('Account')),
                'payment_type':fields.many2one('payment.type', 'Tipo de Pago'),
                'plan_tesoreria_id': fields.many2one('l10n.es.tesoreria.plantilla', 'Plantilla Tesorería'),
                } 

l10n_es_tesoreria_pagos_rece_plan()

class l10n_es_tesoreria_pagos_cash_plan(osv.osv):
    _name = 'l10n.es.tesoreria.pagos.cash.plan'

    _columns = {
                'name': fields.char('Descripción', size=64),
                'fecha': fields.date('Fecha'),
                'diario': fields.many2one('account.journal', 'Diario'),
                'importe': fields.float('Importe', digits_compute=dp.get_precision('Account')),
                'payment_type':fields.many2one('payment.type', 'Tipo de Pago'),
                'type':fields.selection([('in', 'Entrada'),('out','Salida')],'Tipo', required=True),
                'plan_tesoreria_id': fields.many2one('l10n.es.tesoreria.plantilla', 'Plantilla Tesorería'),
    }
l10n_es_tesoreria_pagos_cash_plan()

class l10n_es_tesoreria_pagos_var_plan(osv.osv):
    _inherit = 'l10n.es.tesoreria.pagos.var.plan'
    _columns = {
                'payment_type': fields.many2one('payment.type', 'Tipo de Pago'),
                }
l10n_es_tesoreria_pagos_var_plan()
    
    
class l10n_es_tesoreria_pagos_period_plan(osv.osv):
    _inherit = 'l10n.es.tesoreria.pagos.period.plan'
    _columns = {
                'payment_type': fields.many2one('payment.type', 'Tipo de Pago'),
                }
l10n_es_tesoreria_pagos_period_plan()