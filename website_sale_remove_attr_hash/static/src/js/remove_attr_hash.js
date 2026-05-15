odoo.define("website_sale_remove_attr_hash.fix", function (require) {
  "use strict";

  var publicWidget = require("web.public.widget");
  require("website_sale.website_sale");

  publicWidget.registry.WebsiteSale.include({
    _setUrlHash: function () {
      return;
    },
  });
});
