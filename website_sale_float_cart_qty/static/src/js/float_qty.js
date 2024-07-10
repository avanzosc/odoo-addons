/** @odoo-module **/

import publicWidget from "web.public.widget";
import wSaleUtils from "website_sale.utils";
var core = require("web.core");
require("website_sale.website_sale");

publicWidget.registry.WebsiteSale.include({
  /**
   * Override the _changeCartQuantity method of WebsiteSale
   */
  _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
    console.log("Entering _changeCartQuantity function");

    _.each($dom_optional, function (elem) {
      $(elem).find(".js_quantity").text(value);
      productIDs.push($(elem).find("span[data-product-id]").data("product-id"));
    });
    $input.data("update_change", true);

    value = parseFloat($input.val() || 0);

    this._rpc({
      route: "/shop/cart/update_json",
      params: {
        line_id: line_id,
        product_id: $input.data("product-id"),
        set_qty: value,
      },
    }).then(function (data) {
      data.cart_quantity = parseFloat($input.val() || 0);

      $input.data("update_change", false);
      var check_value = parseFloat($input.val() || 0);
      if (isNaN(check_value)) {
        check_value = 1.0;
      }
      if (value !== check_value) {
        $input.trigger("change");
        return;
      }
      sessionStorage.setItem("website_sale_cart_quantity", data.cart_quantity);
      if (!data.cart_quantity) {
        window.location = "/shop/cart";
        return;
      }
      $input.val(data.quantity);
      $(".js_quantity[data-line-id=" + line_id + "]")
        .val(data.quantity)
        .text(data.quantity);

      if (typeof wSaleUtils !== "undefined") {
        wSaleUtils.updateCartNavBar(data);
        wSaleUtils.showWarning(data.warning);
      }

      core.bus.trigger("cart_amount_changed", data.amount, data.minor_amount);
    });
  },
});
