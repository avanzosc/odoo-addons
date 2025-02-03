import logging

from odoo import http

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

        if not self._validate_payment_mode_id(payment_mode_id):
            return self._redirect_with_message("Payment mode ID is missing", 400)

        if not self._validate_bank_account(new_bank_account):
            return self._redirect_with_message(
                "The bank account number must start with 'ES' followed by 22 digits.",
                400,
            )

        if self._check_existing_bank_account(new_bank_account):
            return self._redirect_with_message(
                "The bank account already exists",
                400,
                existing_bank_id=self.existing_bank_id,
            )

        self._deactivate_existing_bank_accounts()
        self._create_new_bank_account(new_bank_account)

        sale_order_id = self._get_sale_order_id(kwargs)
        if not sale_order_id:
            return self._redirect_with_message("Sale order ID missing", 400)

        sale_order = self._get_sale_order(sale_order_id)
        if not sale_order:
            return self._redirect_with_message("Sale order not found", 400)

        if payment_mode_id:
            self._assign_payment_mode(sale_order, payment_mode_id)

        _logger.info(
            "New bank account created and old ones removed for partner ID: %s.\
                Assigned to order ID: %s",
            http.request.env.user.partner_id.id,
            sale_order_id,
        )

        return self._redirect_with_message("Bank account saved successfully", 200)

    def _validate_payment_mode_id(self, payment_mode_id):
        if not payment_mode_id:
            _logger.warning("Payment mode ID was not provided.")
            return False
        return True

    def _validate_bank_account(self, bank_account):
        bank_account = bank_account.upper() if bank_account else ""
        is_valid = (
            bank_account.startswith("ES")
            and len(bank_account) == 24
            and bank_account[2:].isdigit()
        )
        if not is_valid:
            _logger.warning(
                "The bank account must start with 'ES' followed by 22 digits."
            )
        return is_valid

    def _check_existing_bank_account(self, bank_account):
        self.existing_bank_id = None
        existing_bank = (
            http.request.env["res.partner.bank"]
            .sudo()
            .search([("acc_number", "=", bank_account)], limit=1)
        )
        if existing_bank:
            _logger.warning("The bank account already exists: %s", bank_account)
            self.existing_bank_id = existing_bank.id
            return True
        return False

    def _deactivate_existing_bank_accounts(self):
        partner_id = http.request.env.user.partner_id.id
        http.request.env["res.partner.bank"].sudo().search(
            [("partner_id", "=", partner_id)]
        ).write({"active": False})

    def _create_new_bank_account(self, bank_account):
        partner_id = http.request.env.user.partner_id.id
        http.request.env["res.partner.bank"].sudo().create(
            {
                "acc_number": bank_account,
                "partner_id": partner_id,
            }
        )

    def _get_sale_order_id(self, kwargs):
        return (
            kwargs.get("sale_order_id")
            or http.request.session.get("sale_order_id")
            or http.request.env["website"].sudo().sale_get_order()
        )

    def _get_sale_order(self, sale_order_id):
        sale_order = http.request.env["sale.order"].sudo().browse(sale_order_id)
        if not sale_order.exists():
            _logger.warning("Sale order not found: %s", sale_order_id)
            return None
        return sale_order

    def _assign_payment_mode(self, sale_order, payment_mode_id):
        sale_order.write({"payment_mode_id": int(payment_mode_id)})

    def _redirect_with_message(self, message, status, existing_bank_id=None):
        redirect_url = f"/shop/payment?message={message}&status={status}"
        if existing_bank_id:
            redirect_url += f"&existing_bank_id={existing_bank_id}"
        return http.request.redirect(redirect_url)

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
            return self._json_error("Bank account ID was not provided.")

        try:
            bank_id = int(bank_id)
        except ValueError:
            return self._json_error("The bank account ID is not a valid number.")

        sale_order_id = http.request.session.get("sale_order_id")
        if not sale_order_id:
            return self._json_error("No sale order ID found in the session.")

        sale_order = http.request.env["sale.order"].sudo().browse(sale_order_id)
        if not sale_order.exists():
            return self._json_error("No sale order found with the provided ID.")

        _logger.info(
            "Bank account selected and successfully assigned to order ID: %s",
            sale_order_id,
        )
        return self._json_success(
            "Bank account selected and successfully assigned to the order."
        )

    def _json_error(self, message):
        _logger.warning(message)
        return {"status": "error", "message": message}

    def _json_success(self, message):
        _logger.info(message)
        return {"status": "success", "message": message}

    @http.route(
        "/send_email_to_log_for_existing_account",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def send_email_to_log_for_existing_account(self, **kwargs):
        existing_bank_id = kwargs.get("existing_bank_id")

        if not existing_bank_id:
            return self._json_error("No existing bank ID provided.")

        bank_record = self._get_bank_record(existing_bank_id)
        if not bank_record:
            return self._json_error("Bank account not found.")

        partner = bank_record.partner_id
        if not partner:
            return self._json_error("Associated partner not found.")

        user = partner.user_id
        if not user:
            return self._json_error("User not found for the associated partner.")

        try:
            user.action_reset_password()
            return self._json_success("Password reset email sent successfully.")
        except Exception as e:
            _logger.error("Error sending password reset email: %s", str(e))
            return {"error": str(e)}

    def _get_bank_record(self, bank_id):
        bank_record = (
            http.request.env["res.partner.bank"]
            .sudo()
            .search([("id", "=", bank_id)], limit=1)
        )
        if not bank_record:
            _logger.warning("Bank account not found for ID: %s", bank_id)
        return bank_record
