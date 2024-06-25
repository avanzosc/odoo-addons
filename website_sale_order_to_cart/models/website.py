from odoo import models, SUPERUSER_ID
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    def sale_get_order(self, force_create=False, update_pricelist=False):
        """Return the current sales order after mofications specified by params.

        :param bool force_create: Create sales order if not already existing
        :param bool update_pricelist: Force to recompute all the lines from sales order to adapt the price with the current pricelist.
        :returns: record for the current sales order (might be empty)
        :rtype: `sale.order` recordset
        """
        self.ensure_one()

        self = self.with_company(self.company_id)
        SaleOrder = self.env["sale.order"].sudo()

        sale_order_search = SaleOrder.search(
            [
                ("partner_id", "=", self.env.user.partner_id.id),
                ("state", "=", "draft"),
                ("is_abandoned_cart", "=", True),
            ],
            order="create_date desc",
            limit=1,
        )

        if sale_order_search:
            sale_order_id = sale_order_search[0].id
        else:
            sale_order_id = request.session.get("sale_order_id")

        if sale_order_id:
            sale_order_sudo = SaleOrder.browse(sale_order_id).exists()
            if (
                sale_order_sudo
                and sale_order_sudo.get_portal_last_transaction().state
                in ("pending", "authorized", "done")
            ):
                sale_order_sudo.get_portal_last_transaction().state = "draft"
        elif self.env.user and not self.env.user._is_public():
            sale_order_sudo = self.env.user.partner_id.last_website_so_id
            if sale_order_sudo:
                available_pricelists = self.get_pricelist_available()
                if sale_order_sudo.pricelist_id not in available_pricelists:
                    # Do not reload the cart of this user last visit
                    # if the cart uses a pricelist no longer available.
                    sale_order_sudo = SaleOrder
                else:
                    # Do not reload the cart of this user last visit
                    # if the Fiscal Position has changed.
                    fpos = (
                        sale_order_sudo.env["account.fiscal.position"]
                        .with_company(sale_order_sudo.company_id)
                        ._get_fiscal_position(
                            sale_order_sudo.partner_id,
                            delivery=sale_order_sudo.partner_shipping_id,
                        )
                    )
                    if fpos.id != sale_order_sudo.fiscal_position_id.id:
                        sale_order_sudo = SaleOrder
        else:
            sale_order_sudo = SaleOrder

        # Ignore the current order if a payment has been initiated. We don't want to retrieve the
        # cart and allow the user to update it when the payment is about to confirm it.
        if sale_order_sudo and sale_order_sudo.get_portal_last_transaction().state in (
            "pending",
            "authorized",
            "done",
        ):
            sale_order_sudo = None

        if not (sale_order_sudo or force_create):
            # Do not create a SO record unless needed
            if request.session.get("sale_order_id"):
                request.session.pop("sale_order_id")
                request.session.pop("website_sale_cart_quantity", None)
            return self.env["sale.order"]

        # Only set when neeeded
        pricelist_id = False

        partner_sudo = self.env.user.partner_id

        # cart creation was requested
        if not sale_order_sudo:
            so_data = self._prepare_sale_order_values(partner_sudo)
            sale_order_sudo = SaleOrder.with_user(SUPERUSER_ID).create(so_data)

            request.session["sale_order_id"] = sale_order_sudo.id
            request.session["website_sale_cart_quantity"] = (
                sale_order_sudo.cart_quantity
            )
            # The order was created with SUPERUSER_ID, revert back to request user.
            sale_order_sudo = sale_order_sudo.with_user(self.env.user).sudo()
            return sale_order_sudo

        # Existing Cart:
        #   * For logged user
        #   * In session, for specified partner

        # case when user emptied the cart
        if not request.session.get("sale_order_id"):
            request.session["sale_order_id"] = sale_order_sudo.id
            request.session["website_sale_cart_quantity"] = (
                sale_order_sudo.cart_quantity
            )

        # check for change of partner_id ie after signup
        if (
            sale_order_sudo.partner_id.id != partner_sudo.id
            and request.website.partner_id.id != partner_sudo.id
        ):
            previous_fiscal_position = sale_order_sudo.fiscal_position_id
            previous_pricelist = sale_order_sudo.pricelist_id

            # Reset the session pricelist according to logged partner pl
            request.session.pop("website_sale_current_pl", None)
            pricelist_id = self._get_current_pricelist_id(partner_sudo)
            request.session["website_sale_current_pl"] = pricelist_id

            # change the partner, and trigger the computes (fpos)
            sale_order_sudo.write(
                {
                    "partner_id": partner_sudo.id,
                    "partner_invoice_id": partner_sudo.id,
                    "payment_term_id": self.sale_get_payment_term(partner_sudo),
                    # Must be specified to ensure it is not recomputed when it shouldn't
                    "pricelist_id": pricelist_id,
                }
            )

            if sale_order_sudo.fiscal_position_id != previous_fiscal_position:
                sale_order_sudo.order_line._compute_tax_id()

            if sale_order_sudo.pricelist_id != previous_pricelist:
                update_pricelist = True
        elif update_pricelist:
            # Only compute pricelist if needed
            pricelist_id = self._get_current_pricelist_id(partner_sudo)

        # update the pricelist
        if update_pricelist:
            request.session["website_sale_current_pl"] = pricelist_id
            sale_order_sudo.write({"pricelist_id": pricelist_id})
            sale_order_sudo._recompute_prices()

        return sale_order_sudo


