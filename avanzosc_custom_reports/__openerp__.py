# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "Custom Reports for Avanzosc",
    "summary": "",
    "version": "1.0",
    "category": "Custom Module",
    "license": "AGPL-3",
    "author": "AvanzOSC, "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    "website": "http://www.odoomrp.com",
    "contributors": [
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Esther Martín <esthermartin@avanzosc.es>",
    ],
    "depends": [
        "sale",
        "sale_order_project",
        "event",
        "event_track_assistant",
        "report",
    ],
    "data": [
        "templates/sale_order_templates.xml",
        "templates/event_template.xml",
        "data/report_paperformat.xml",
    ],
    "installable": True,
}
