console.log("List Renderer heredado");

odoo.define("custom_list_renderer_limit.list_renderer", function (require) {
  "use strict";
  
  console.log("List Renderer heredado");

  var ListRenderer = require("web.ListRenderer");

  ListRenderer.include({
    init: function () {
      this._super.apply(this);
      this.limit = 100;
    },
  });
});
