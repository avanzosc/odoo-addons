import DevicesSynchronisation from "@point_of_sale/app/store/devices_synchronisation";
import {Domain} from "@web/core/domain";
import {PosData} from "@point_of_sale/app/models/data_service";
import {PosStore} from "@point_of_sale/app/store/pos_store";
import {patch} from "@web/core/utils/patch";

function getSessionDateStr(session) {
  const startAt = session && session.start_at;
  if (startAt) {
    return String(startAt).slice(0, 10) + " 00:00:00";
  }
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, "0");
  const dd = String(today.getDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd} 00:00:00`;
}

patch(PosData.prototype, {
  async preLoadData(data) {
    const result = await super.preLoadData(data);

    if (!result["pos.order"]) {
      return result;
    }

    const session = this.models["pos.session"]?.getFirst?.();
    const dateStr = getSessionDateStr(session);

    result["pos.order"] = result["pos.order"].filter((r) => {
      if (!r.date_order) {
        return false;
      }
      const d = String(r.date_order);
      const normalized = d.includes("T")
        ? d.slice(0, 10) + " " + d.slice(11, 19)
        : d.slice(0, 19);
      return normalized >= dateStr;
    });

    const todayOrderIds = new Set(
      result["pos.order"].map((o) => o.id).filter((id) => typeof id === "number")
    );

    if (result["pos.order.line"]) {
      result["pos.order.line"] = result["pos.order.line"].filter(
        (l) => typeof l.order_id !== "number" || todayOrderIds.has(l.order_id)
      );
    }

    if (result["pos.payment"]) {
      result["pos.payment"] = result["pos.payment"].filter(
        (p) => typeof p.pos_order_id !== "number" || todayOrderIds.has(p.pos_order_id)
      );
    }

    if (result["pos.pack.operation.lot"]) {
      const todayLineIds = new Set(
        (result["pos.order.line"] || [])
          .map((l) => l.id)
          .filter((id) => typeof id === "number")
      );
      result["pos.pack.operation.lot"] = result["pos.pack.operation.lot"].filter(
        (l) =>
          typeof l.pos_order_line_id !== "number" ||
          todayLineIds.has(l.pos_order_line_id)
      );
    }

    return result;
  },
});

patch(PosStore.prototype, {
  async getServerOrders() {
    const domain = [
      ["config_id", "in", [...this.config.raw.trusted_config_ids, this.config.id]],
      ["state", "=", "draft"],
      ["date_order", ">=", getSessionDateStr(this.session)],
    ];
    return await this.loadServerOrders(domain);
  },
});

patch(DevicesSynchronisation.prototype, {
  constructOrdersDomain() {
    const skipModels = [
      "pos.order",
      "pos.order.line",
      "pos.payment",
      "pos.pack.operation.lot",
    ];
    skipModels.forEach((m) => this.dynamicModels.delete(m));
    const result = super.constructOrdersDomain();
    skipModels.forEach((m) => this.dynamicModels.add(m));

    const dateStr = getSessionDateStr(this.pos.session);
    const config = this.pos.config;

    result.domain["pos.order"] = new Domain([
      ["state", "=", "draft"],
      ["date_order", ">=", dateStr],
      ["config_id", "in", [config.id, ...config.trusted_config_ids]],
    ]).toList();
    result.recordsIds["pos.order"] = [];

    return result;
  },
});
