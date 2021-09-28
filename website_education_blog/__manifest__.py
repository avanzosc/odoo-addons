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
        "website",
        "website_blog",
        "contacts_school",
        "contacts_school_education",
    ],
    "data": [
        "security/blog_rules.xml",
        "views/blog_blog_view.xml",
        "views/blog_post_view.xml",
        "views/views.xml",
    ],
    "installable": True,
}
