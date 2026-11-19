{
    "name": "Login as Sale Salesperson",
    "version": "18.0.1.0.0",
    "author": "Atharva Systems",
    "license": "AGPL-3",
    "category": "Tools",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["website", "sale_management", "website_sale"],
    "data": [
        "views/res_users_view.xml",
        "views/webclient_templates.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "qweb": [],
    "assets": {
        "web.assets_frontend": [
            "as_login_as_salesperson/static/src/js/login_as.js",
        ],
    },
    "installable": True,
}
