
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2008-2012 Daniel (AvanzOSC). All Rights Reserved
#    11/07/2012
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
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


{
    'name': 'Asset Amortize',
    'version': "1.2",
    'category': "Generic Modules",
    'author': 'AvanzOSC',
    'website': 'www.avanzosc.com',
    'depends': ['l10n_es_account_asset'],
    'init_xml': [],
    'update_xml': ['asset_view.xml',
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
    'description': """
                    This module allows to depreciate as percentage.
                    Adds fiscal depreciation Board
 		""",
}

