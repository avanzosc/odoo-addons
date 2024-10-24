import logging

from odoo import _, http

_logger = logging.getLogger(__name__)


class PaymentController(http.Controller):
    @http.route(
        "/create_new_bank_account",
        type="http",
        auth="user",
        methods=["POST"],
        csrf=False,
        website=True,
    )
    def create_new_bank_account(self, **kwargs):
        new_bank_account = kwargs.get("new_bank_account")
        payment_mode_id = kwargs.get("payment_mode_id")

        msg_payment_mode_missing = _("Payment mode ID is missing")
        msg_invalid_bank_account = _(
            "The bank account number must start with 'ES' followed by 22 digits."
        )
        msg_bank_account_exists = _("The bank account already exists")
        msg_success = _("Bank account saved successfully")

        if not payment_mode_id:
            _logger.warning("Payment mode ID was not provided.")
            return http.request.redirect(
                f"/shop/payment?message={msg_payment_mode_missing}&status=400"
            )

        # Convert the bank account to uppercase
        new_bank_account = new_bank_account.upper()

        # Validate that the bank account starts with 'ES' and is followed by exactly 22 digits
        if not (
            new_bank_account.startswith("ES")
            and len(new_bank_account) == 24
            and new_bank_account[2:].isdigit()
        ):
            _logger.warning(
                "The bank account must start with 'ES' followed by 22 digits."
            )
            return http.request.redirect(
                f"/shop/payment?message={msg_invalid_bank_account}&status=400"
            )

        existing_bank = (
            http.request.env["res.partner.bank"]
            .sudo()
            .search([("acc_number", "=", new_bank_account)], limit=1)
        )

        if existing_bank:
            _logger.warning("The bank account already exists: %s", new_bank_account)
            return http.request.redirect(
                f"/shop/payment?message={msg_bank_account_exists}&status=400"
            )

        partner_id = http.request.env.user.partner_id.id

        # Remove any existing bank accounts for this partner
        http.request.env["res.partner.bank"].sudo().search(
            [("partner_id", "=", partner_id)]
        ).unlink()

        # Create the new bank account
        
        http.request.env["res.partner.bank"].sudo().create(
            {
                "acc_number": new_bank_account,
                "partner_id": partner_id,
            }
        )
    

        # Retrieve the sale_order_id from the session
        sale_order_id = (
            kwargs.get("sale_order_id")
            or http.request.session.get("sale_order_id")
            or http.request.env["website"].sudo().sale_get_order()
        )
        if not sale_order_id:
            _logger.warning("Sale order ID was not provided.")
            return http.request.redirect(
                "/shop/payment?message=Sale order ID missing&status=400"
            )

        sale_order = http.request.env["sale.order"].sudo().browse(sale_order_id)
        if not sale_order.exists():
            _logger.warning("Sale order not found: %s", sale_order_id)
            return http.request.redirect(
                "/shop/payment?message=Sale order not found&status=400"
            )

        if sale_order and payment_mode_id:
            sale_order.write(
                {
                    "payment_mode_id": int(payment_mode_id),
                }
            )

        _logger.info(
            "New bank account created and old ones\
                removed for partner ID: %s. Assigned to order ID: %s",
            partner_id,
            sale_order_id,
        )

        return http.request.redirect(f"/shop/payment?message={msg_success}&status=200")

    @http.route(
        "/choose_bank_account",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
        website=True,
    )
    def choose_bank_account(self, bank_id=None, **kwargs):
        if not bank_id:
            _logger.warning("Bank account ID was not provided.")
            return {
                "status": "error",
                "message": "Bank account ID was not provided.",
            }

        try:
            bank_id = int(bank_id)
        except ValueError:
            _logger.error("The bank account ID is not a valid number: %s", bank_id)
            return {
                "status": "error",
                "message": "The bank account ID is not a valid number.",
            }

        sale_order_id = http.request.session.get("sale_order_id")
        if not sale_order_id:
            _logger.warning("No sale order ID found in the session.")
            return {
                "status": "error",
                "message": "No sale order ID found in the session.",
            }

        sale_order = http.request.env["sale.order"].sudo().browse(sale_order_id)
        if not sale_order.exists():
            _logger.warning("No sale order found with ID: %s", sale_order_id)
            return {
                "status": "error",
                "message": "No sale order found with the provided ID.",
            }

        # sale_order.write({"bank_account_id": bank_id})
        _logger.info(
            "Bank account selected and successfully assigned to order ID: %s",
            sale_order_id,
        )

        return {
            "status": "success",
            "message": "Bank account selected and successfully assigned to the order.",
        }
