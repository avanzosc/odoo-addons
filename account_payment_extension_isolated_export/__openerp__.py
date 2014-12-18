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
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

{
    "name": "Account Payment Extension Isolated Export",
    "version": "1.0",
    "depends": ["account_payment_extension",
                "account_payment_export",
                "l10n_es_payment_order"],
    "author": "AvanzOSC",
    "category": "Banking",
    "description": """
        This module isolates a payment order file export from payment done
        process and creates a new button for it.
    """,
    "init_xml": [],
    'update_xml': ["views/account_payment_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
