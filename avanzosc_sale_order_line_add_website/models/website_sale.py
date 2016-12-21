# -*- coding: utf-8 -*-
# © 2016 AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class WebsiteSale(models.Model):
    _name = 'website.sale'

    name = fields.Char(string='Name')
