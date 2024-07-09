from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    forwarder_id = fields.Many2one(
        "res.partner",
        string="Forwarder", 
        domain="[('is_company', '=', True)]",
        help="Transport service provider."
    )
    carrier_id = fields.Many2one(
        "purchase.order.carrier",
        string="Carrier",
        help="Company responsible for the shipment."
    )
    pol_id = fields.Many2one(
        "res.country.state", 
        string="Port of Origin (POL)",
        help="Port from which the goods depart."
    )
    pod_id = fields.Many2one(
        "res.country.state", 
        string="Port of Destination (POD)",
        help="Port of arrival of the goods."
    )
    date_sent = fields.Date(
        string="Date Sent",
        help="Date the email is sent to the supplier."
    )
    cargo_ready = fields.Date(
        string="Cargo Ready Date",
        help="Date when the supplier confirms that the material will be finished."
    )
    cut_off = fields.Date(
        string="Cut-off Date",
        help="Deadline to deliver the material so it can be loaded onto that ship."
    )
    date_etd = fields.Date(
        string="Estimated Time of Departure (ETD)",
        help="Date of departure from port of the container."
    )
    date_eta = fields.Date(
        string="Estimated Time of Arrival (ETA)",
        help="Date of arrival of the container at port."
    )
