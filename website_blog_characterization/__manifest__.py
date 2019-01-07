# Copyright 2018 Gotzon Imaz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Website Blog Characterization",
    "version": "11.0.2.0.0",
    "category": "Website",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "depends": [
        "website_blog",
        "base_characterization",
        "mass_mailing",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/blog_post_view.xml",
        "views/mail_mass_mailing_blog_post_view.xml",
        "views/mail_mass_mailing_view.xml",
        "wizards/mail_mass_mailing_post_wizard_view.xml",
    ],
    "installable": True,
}
