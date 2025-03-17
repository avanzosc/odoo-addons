odoo.define("mail_ir_attachment_kanban.AttachmentCardHoverInfo", function (require) {
  "use strict";

  const {patch} = require("@web/core/utils/patch");
  const {AttachmentCard} = require("@mail/components/attachment_card/attachment_card");
  const {onMounted, onWillUnmount} = require("@odoo/owl");

  patch(AttachmentCard.prototype, "mail_ir_attachment_kanban.AttachmentCardHoverInfo", {
    setup() {
      this._super(...arguments);
      this._tooltip = null;

      onMounted(() => {
        this._bindHoverEvent();
      });

      onWillUnmount(() => {
        this._unbindHoverEvent();
      });
    },

    _bindHoverEvent() {
      const attachmentId =
        this.props.record && this.props.record.attachment
          ? this.props.record.attachment.id
          : null;
      if (!attachmentId) {
        return;
      }

      const attachmentCard = document.querySelector(
        `.o_AttachmentCard[attachment-id="${attachmentId}"]`
      );
      if (!attachmentCard) {
        return;
      }

      this._onMouseEnter = () => this._onHoverStart(attachmentId, attachmentCard);
      this._onMouseLeave = () => this._onHoverEnd();

      attachmentCard.addEventListener("mouseenter", this._onMouseEnter);
      attachmentCard.addEventListener("mouseleave", this._onMouseLeave);
    },

    _unbindHoverEvent() {
      let attachmentId = null;
      try {
        if (this.props && this.props.record && this.props.record.attachment) {
          attachmentId = this.props.record.attachment.id;
        } else {
          console.error("Error al acceder a attachment.id:");
          return;
        }
      } catch (error) {
        console.error("Error al acceder a attachment.id:", error);
        return;
      }

      const attachmentCard = document.querySelector(
        `.o_AttachmentCard[attachment-id="${attachmentId}"]`
      );
      if (!attachmentCard) {
        return;
      }

      attachmentCard.removeEventListener("mouseenter", this._onMouseEnter);
      attachmentCard.removeEventListener("mouseleave", this._onMouseLeave);
    },

    async _onHoverStart(attachmentId, attachmentCard) {
      if (!attachmentId) {
        return;
      }
      await this._fetchAttachmentInfo(attachmentId, attachmentCard);
    },

    _onHoverEnd() {
      this._hideTooltip();
    },

    async _fetchAttachmentInfo(attachmentId, attachmentCard) {
      try {
        const attachmentData = await this.env.services.orm.call(
          "ir.attachment",
          "read",
          [[attachmentId], ["create_date", "create_uid", "write_date", "write_uid"]],
          {}
        );

        if (attachmentData && attachmentData.length > 0) {
          const attachment = attachmentData[0];
          const info = `
          <strong>Creado:</strong> ${attachment.create_date} por <em>${
            (attachment.create_uid && attachment.create_uid[1]) || "Desconocido"
          }</em><br>
          <strong>Modificado:</strong> ${attachment.write_date} por <em>${
            (attachment.write_uid && attachment.write_uid[1]) || "Desconocido"
          }</em>
          `;
          this._showTooltip(info, attachmentCard);
        }
      } catch (error) {
        console.error("Error fetching attachment info:", error);
      }
    },

    _showTooltip(info, attachmentCard) {
      if (!this._tooltip) {
        this._tooltip = document.createElement("div");
        this._tooltip.id = "attachment-hover-tooltip";
        this._tooltip.style.position = "absolute";
        this._tooltip.style.background = "#fff";
        this._tooltip.style.border = "1px solid #ccc";
        this._tooltip.style.padding = "10px 15px";
        this._tooltip.style.zIndex = "1000";
        this._tooltip.style.pointerEvents = "none";
        this._tooltip.style.fontSize = "14px";
        this._tooltip.style.fontFamily = "'Arial', sans-serif";
        this._tooltip.style.color = "#333";
        this._tooltip.style.borderRadius = "5px";
        this._tooltip.style.boxShadow = "0 2px 10px rgba(0, 0, 0, 0.1)";
        this._tooltip.style.maxWidth = "200px";
        this._tooltip.style.textAlign = "center";
        this._tooltip.style.lineHeight = "1.5";
        document.body.appendChild(this._tooltip);
      }

      const rect = attachmentCard.getBoundingClientRect();
      this._tooltip.innerHTML = info;
      this._tooltip.style.left = `${rect.left}px`;
      this._tooltip.style.top = `${rect.bottom + 5}px`;
      this._tooltip.style.display = "block";
    },

    _hideTooltip() {
      if (this._tooltip) {
        this._tooltip.style.display = "none";
      }
    },
  });
});
