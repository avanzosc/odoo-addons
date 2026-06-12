/* global console, FormData, fetch, window */
import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

publicWidget.registry.WebsiteCustomSaca = publicWidget.Widget.extend({
  selector: "#driver_saca_edit, .saca_line_card",
  events: {
    "click #btn_saca_edit_2": "_onBtnSacaEdit2Click",
    "click #btn_saca_edit": "_onBtnSacaEditClick",
    "click #btn_saca_send": "_onBtnSacaSendClick",
    "change .ticket_upload": "_onTicketUploadChange",
    "click #upload_img": "_onUploadImgClick",
  },

  start: function () {
    this._checkCheckboxes();
    return this._super.apply(this, arguments);
  },

  _checkCheckboxes: function () {
    const chboxes = this.$("input.checked");
    if (chboxes.length > 0) {
      chboxes.attr("checked", true);
    }
  },

  _onBtnSacaEdit2Click: function () {
    this.$("#btn_saca_edit").trigger("click");
  },

  _onBtnSacaEditClick: function () {
    const first = this.$(".weight_input")[0];
    if (first && this.$(first).css("display") === "none") {
      this.$(".info_span").css("display", "none");
      this.$(".weight_input").css("display", "block");
      this.$(".saca_input").css("display", "initial");
      this.$(".saca_input_file").css("display", "initial");
      this.$(".unload_input").css("display", "initial");
      this.$("#btn_saca_save").css("display", "block");
      this.$("#btn_saca_save_2").css("display", "block");
      this.$("#btn_saca_edit").css("display", "none");
      this.$("#btn_saca_edit_2").css("display", "none");
      this.$("#img_origin").css("display", "block");
      this.$("#img_dest").css("display", "block");
      this.$("#chbx_fork").removeAttr("disabled");
    } else {
      this.$(".info_span").css("display", "block");
      this.$(".weight_input").css("display", "none");
      this.$(".unload_input").css("display", "none");
      this.$(".saca_input").css("display", "none");
      this.$(".saca_input_file").css("display", "none");
      this.$(".chbx_fork").attr("disabled", "disabled");
      this.$("#img_origin").css("display", "none");
      this.$("#img_dest").css("display", "none");
    }
  },

  _onBtnSacaSendClick: function (ev) {
    const id = ev.currentTarget.getAttribute("value");
    rpc("/saca/line/send/" + id, {}).then(function (result) {
      console.log(result);
    });
  },

  _onTicketUploadChange: function (ev) {
    this.$(ev.currentTarget).prev("button").css("display", "block");
  },

  _onUploadImgClick: function (ev) {
    const fileInput = this.$(ev.currentTarget).next("input");
    const sacaLineId = this.$("#current_saca_line").val();
    const formData = new FormData();
    formData.append("image_field", fileInput.attr("name"));
    const files = fileInput.prop("files");
    if (files && files.length > 0) {
      formData.append("image_file", files[0]);
    }
    const csrfInput = this.$('input[name="csrf_token"]').val();
    if (csrfInput) {
      formData.append("csrf_token", csrfInput);
    }
    fetch("/my/saca/line/" + sacaLineId + "/binary", {
      method: "POST",
      body: formData,
    }).then(function () {
      window.location.href = "/my/saca/line/" + sacaLineId;
    });
  },
});

export default publicWidget.registry.WebsiteCustomSaca;
