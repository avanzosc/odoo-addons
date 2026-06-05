# Copyright Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Quant Purchase FIFO Valuation (Not Traceable)",
    "version": "18.0.1.0.0",
    "category": "Inventory",
    "summary": "Export XLSX from selected Quants: non‑traceable vs purchase lines.",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "website": "https://github.com/avanzosc/odoo-addons",
    "depends": ["purchase", "stock", "purchase_order_shipping_method"],
    "data": [
        "data/ir_actions_server.xml",
    ],
    "installable": True,
}
