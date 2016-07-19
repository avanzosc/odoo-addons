# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Partner Student Course",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Customer Relationship Managementt",
    "depends": [
        'partner_contact_birthdate',
    ],
    "data": [
        'security/partner_student_course.xml',
        'security/ir.model.access.csv',
        'views/partner_student_course_view.xml',
        'views/res_partner_view.xml',
    ],
    "installable": True,
    "auto_install": False,
}
