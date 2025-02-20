{
    "name": "Account Move DB Wizard",
    "version": "1.0",
    "summary": "Connects to a remote DB and fetches account move line data",
    "author": "Your Name",
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/connect_db_wizard_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "connect_db_wizard/static/src/js/**/*",
        ],
    },
    "external_dependencies": {"python": ["sshtunnel"]},
    "installable": True,
    "application": False,
}
