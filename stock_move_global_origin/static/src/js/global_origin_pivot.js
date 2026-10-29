odoo.define("stock_move_global_origin.PivotRenderer", function (require) {
  "use strict";

  const PivotRenderer = require("web.PivotRenderer");

  const STATE_ROW_INDENT = 4;
  const STATE_COLOR_MAP = {
    cancel: "o_go_state_cancel",
    done: "o_go_state_done",
  };
  const STATE_COLOR_CLASSES = [
    "o_go_state_done",
    "o_go_state_pending",
    "o_go_state_cancel",
  ];

  class GlobalOriginPivotRenderer extends PivotRenderer {
    mounted() {
      super.mounted();
      this.el.classList.add("o_global_origin_pivot");
      this._colorStateRows();
    }
    patched() {
      super.patched();
      this.el.classList.add("o_global_origin_pivot");
      this._colorStateRows();
    }

    _colorStateRows() {
      const trs = this.el.querySelectorAll("tbody tr");
      trs.forEach((tr) => tr.classList.remove(...STATE_COLOR_CLASSES));
      this.props.table.rows.forEach((row, index) => {
        if (row.indent !== STATE_ROW_INDENT) {
          return;
        }
        const rawValues = row.groupId && row.groupId[0];
        const state = rawValues && rawValues[rawValues.length - 1];
        const colorClass = STATE_COLOR_MAP[state] || "o_go_state_pending";
        const tr = trs[index];
        if (tr) {
          tr.classList.add(colorClass);
        }
      });
    }
  }

  return GlobalOriginPivotRenderer;
});

odoo.define("stock_move_global_origin.PivotView", function (require) {
  "use strict";

  const PivotView = require("web.PivotView");
  const viewRegistry = require("web.view_registry");
  const GlobalOriginPivotRenderer = require("stock_move_global_origin.PivotRenderer");

  const GlobalOriginPivotView = PivotView.extend({
    config: Object.assign({}, PivotView.prototype.config, {
      Renderer: GlobalOriginPivotRenderer,
    }),
  });

  viewRegistry.add("global_origin_pivot", GlobalOriginPivotView);

  return GlobalOriginPivotView;
});
