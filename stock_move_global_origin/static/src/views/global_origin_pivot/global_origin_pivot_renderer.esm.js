/** @odoo-module **/

import {PivotRenderer} from "@web/views/pivot/pivot_renderer";
import {pivotView} from "@web/views/pivot/pivot_view";
import {registry} from "@web/core/registry";

const STATE_ROW_CLASSES = {
  cancel: "o_go_state_cancel",
  done: "o_go_state_done",
};

export class GlobalOriginPivotRenderer extends PivotRenderer {
  static template = "stock_move_global_origin.PivotRenderer";

  /**
   * Colour the rows of the "Status" grouping, whatever level it is at.
   *
   * @param {Object} row
   * @returns {String}
   */
  getStateRowClass(row) {
    if (!row.indent) {
      return "";
    }
    const groupBy = this.model.metaData.fullRowGroupBys[row.indent - 1];
    if (groupBy.split(":")[0] !== "state") {
      return "";
    }
    const state = row.groupId[0][row.indent - 1];
    return STATE_ROW_CLASSES[state] || "o_go_state_pending";
  }
}

registry.category("views").add("global_origin_pivot", {
  ...pivotView,
  Renderer: GlobalOriginPivotRenderer,
});
