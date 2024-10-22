{
    "name": "Mail Chatter Statistics",
    "version": "14.0.1.0.0",
    "author": "Avanzosc",
    "summary": "Add email tracking functionality to Odoo chatter.",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "LGPL-3",
    "depends": ["mail", "mass_mailing"],
    "data": [
        "views/assets.xml",
        "views/mailing_trace_views.xml",
        "views/mail_mail_views.xml",
    ],
    "qweb": ["static/src/xml/chatter_inherit.xml"],
    "installable": True,
    "application": False,
}
