/* @odoo-module */

import {PivotModel} from "@web/views/pivot/pivot_model";
import {patch} from "@web/core/utils/patch";

patch(PivotModel.prototype, {
  _getTableRows(tree, columns) {
    if (
      this.metaData.resModel === "account.invoice.report" &&
      !this.metaData.sortedColumn
    ) {
      const level = tree.root.values.length;
      const groupBy = this.metaData.fullRowGroupBys[level];

      if (groupBy && groupBy.split(":")[0] === "move_id") {
        tree.sortedKeys = [...tree.directSubTrees.keys()].sort((a, b) => {
          const labelA = String(tree.directSubTrees.get(a).root.labels.at(-1) ?? "");

          const labelB = String(tree.directSubTrees.get(b).root.labels.at(-1) ?? "");

          return labelA.localeCompare(labelB, "es", {
            numeric: true,
            sensitivity: "base",
          });
        });
      }
    }

    return super._getTableRows(tree, columns);
  },
});
