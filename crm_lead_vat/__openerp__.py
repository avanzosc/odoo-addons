# -*- coding: utf-8 -*-
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "VAT in Leads",
    "version": "8.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "AvanzOSC, "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Antiun Ingeniería, "
              "S.L.,Odoo Community Association (OCA)",
    "website": "https://odoo-community.org/",
    "license": "AGPL-3",
    "contributors": [
        "Rafael Blasco <rafaelbn@antiun.com>",
        "Jairo Llopis <yajo.sk8@gmail.com>",
        "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "depends": [
        "base_vat",
        "crm",
    ],
    "data": [
        "views/crm_lead_view.xml",
    ],
    "installable": True,
    "application": False,
}
