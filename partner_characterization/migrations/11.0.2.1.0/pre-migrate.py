# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html


def migrate(cr, version):
    if not version:
        return

    cr.execute('DROP TABLE rel_partner_area')
