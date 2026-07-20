/** @odoo-module **/

import {registry} from "@web/core/registry";
import {pivotView} from "@web/views/pivot/pivot_view";
import {PivotRenderer} from "@web/views/pivot/pivot_renderer";

export class TreasuryForecastPivotColorRenderer extends PivotRenderer {
  static template = "treasury_forecast_pivot_color.PivotRenderer";
}

registry.category("views").add("treasury_forecast_pivot_color", {
  ...pivotView,
  Renderer: TreasuryForecastPivotColorRenderer,
});
