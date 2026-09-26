/** @odoo-module **/
/* eslint-disable */

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.AsSalePerson = publicWidget.Widget.extend({
  selector: ".as_sale_person",
  events: {
    "click .login_as_another_btn": "_onAsLoginClick",
  },
  start() {
    console.log("[AsSalePerson] mounted");
    return this._super(...arguments);
  },
  _onAsLoginClick(ev) {
    ev.preventDefault();
    const btn = ev.currentTarget;
    const name = btn.getAttribute("data-login") || "";
    const form = btn.closest("form");
    if (!form) {
      return;
    }
    if (!confirm(`You will be Login As User ${name}`)) {
      return;
    }
    form.submit();
  },
});
