# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def assign_product_attribute_code(cr):
    cr.execute('ALTER TABLE product_attribute '
               'ADD COLUMN attribute_code character varying;')
    cr.execute('UPDATE product_attribute '
               'SET attribute_code = concat(\'AT\', id);')
