// eslint-disable-next-line jsdoc/check-tag-names
/** @odoo-module **/
import "@website_sale/js/website_sale_price_range_option";
import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

publicWidget.registry.CatalogPriceFilter =
  publicWidget.registry.multirangePriceSelector.extend({
    selector: ".o_catalog_detail_page",
    events: {
      'newRangeValue input[type="range"][multiple]': "_onPriceRangeSelected",
    },

    /**
     * Keep the current catalog filters and only update the price range.
     *
     * @private
     * @param {Event} ev
     */
    _onPriceRangeSelected(ev) {
      const range = ev.currentTarget;
      const currentWindow = this.el.ownerDocument.defaultView;
      const url = new currentWindow.URL(currentWindow.location.href);
      const searchParams = url.searchParams;
      const minValue = parseFloat(range.valueLow);
      const maxValue = parseFloat(range.valueHigh);

      searchParams.delete("min_price");
      searchParams.delete("max_price");
      searchParams.delete("page");
      if (parseFloat(range.min) !== minValue) {
        searchParams.set("min_price", range.valueLow);
      }
      if (parseFloat(range.max) !== maxValue) {
        searchParams.set("max_price", range.valueHigh);
      }

      this.el.querySelector("#catalog_products_grid")?.classList.add("opacity-50");
      url.pathname = url.pathname.replace(/\/page\/\d+\/?$/, "");
      currentWindow.location.href = url.toString();
    },
  });

publicWidget.registry.CatalogLayoutSelector = publicWidget.Widget.extend({
  selector: ".o_catalog_detail_page, .o_catalogs_page",
  disabledInEditableMode: false,
  events: {
    "change .o_catalog_apply_layout input": "_onApplyLayoutChange",
  },

  /**
   * @private
   * @param {Event} ev
   */
  _onApplyLayoutChange(ev) {
    const group = ev.target.closest(".o_catalog_apply_layout");
    const target = this.el.querySelector(group.dataset.layoutTarget);
    if (!target) {
      return;
    }

    const isList = ev.target.value === "list";
    const activeClasses = (group.dataset.activeClasses || "active").split(" ");

    for (const button of group.querySelectorAll(".btn")) {
      button.classList.remove(...activeClasses);
    }
    ev.target.nextElementSibling?.classList.add(...activeClasses);

    target.querySelectorAll("*").forEach((el) => {
      el.style.transition = "none";
    });
    target.classList.toggle("o_catalog_layout_list", isList);
    target.getBoundingClientRect();
    target.querySelectorAll("*").forEach((el) => {
      el.style.transition = "";
    });

    if (!this.editableMode) {
      rpc("/catalog/save_layout_mode", {
        page: group.dataset.layoutPage || "catalog_detail",
        layout_mode: isList ? "list" : "grid",
      });
    }
  },
});
