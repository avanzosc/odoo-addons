
# -*- encoding: utf-8 -*-
##############################################################################
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

from openerp import models, fields


class InvoiceGroup(models.Model):

    _name = "account.invoice.group"

    name = fields.Char(string="Group")
    delay = fields.Integer(string="Delay")
    partner_ids = fields.One2many('res.partner', 'invoicing_group',
                                  string="Partners")


class ResPartner(models.Model):

    _inherit = 'res.partner'

    invoicing_group = fields.Many2one('account.invoice.group',
                                      string='Invoicing Group')
