# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Education Blogs",
    "version": "12.0.1.0.0",
    "category": "Website",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "portal",
        "education",
        "website_blog",
        "contacts_school_education",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/blog_rules.xml",
        "views/views.xml",
    ],
    "installable": True,
}
