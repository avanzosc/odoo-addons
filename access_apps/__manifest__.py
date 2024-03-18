# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Control access to Apps""",
    "summary": """You can configure administrators which don't have access to Apps""",
    "category": "Access",
    # "live_test_url": "",
    "images": [],
    "version": "12.0.1.3.3",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@itpp.dev",
    "website": "https://apps.odoo.com/apps/modules/12.0/access_apps/",
    "license": "Other OSI approved licence",  # MIT
    "price": 10.00,
    "currency": "EUR",
    "depends": ["web_settings_dashboard", "access_restricted"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "views/access_apps.xml",
        "security/access_apps_security.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
