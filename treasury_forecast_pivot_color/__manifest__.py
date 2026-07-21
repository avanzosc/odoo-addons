# Copyright 2026 AvanzOSC - Aner Arregi
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Previsión de tesorería: colores en pivot",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "summary": (
        "CLM15016 - Colorea por signo los valores del pivot de previsión de "
        "tesorería (verde positivos, rojo negativos)."
    ),
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        "web",
        "treasury_forecast",
    ],
    "data": [
        "views/treasury_forecast_pivot_views.xml",
    ],
    "assets": {
        # En Odoo 18 el web saca pivot/** de web.assets_backend y lo emite en
        # web.assets_backend_lazy (code-splitting). Si lo añadiéramos en
        # assets_backend nos saldrían los errores "Missing (primary) parent
        # templates: web.PivotRenderer" y módulos no definidos.
        "web.assets_backend_lazy": [
            "treasury_forecast_pivot_color/static/src/pivot/treasury_forecast_pivot_renderer.esm.js",
            "treasury_forecast_pivot_color/static/src/pivot/treasury_forecast_pivot_renderer.xml",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
