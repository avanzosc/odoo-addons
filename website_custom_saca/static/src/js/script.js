odoo.define("website_custom_saca.script", function (require) {
  "use strict";
  var ajax = require("web.ajax");

  check_checkboxes();

  function check_checkboxes() {
    var chboxes = $("input.checked");
    if (chboxes.length > 0) {
      $(chboxes).attr("checked", true);
    }
  }

  $("#btn_saca_edit_2").click(function () {
    $("#btn_saca_edit").trigger("click");
  });
  $("#btn_saca_edit").click(function () {
    var first = $(".weight_input")[0];
    if ($(first).css("display") == "none") {
      $(".info_span").css("display", "none");
      $(".weight_input").css("display", "block");
      $(".saca_input").css("display", "initial");
      $(".saca_input_file").css("display", "initial");
      $(".unload_input").css("display", "initial");
      $("#btn_saca_save").css("display", "block");
      $("#btn_saca_save_2").css("display", "block");
      $("#btn_saca_edit").css("display", "none");
      $("#btn_saca_edit_2").css("display", "none");
      $("#img_origin").css("display", "block");
      $("#img_dest").css("display", "block");
      $("#chbx_fork").removeAttr("disabled");
    } else {
      $(".info_span").css("display", "block");
      $(".weight_input").css("display", "none");
      $(".unload_input").css("display", "none");
      $(".saca_input").css("display", "none");
      $(".saca_input_file").css("display", "none");
      $(".chbx_fork").attr("disabled", "disabled");
      $("#img_origin").css("display", "none");
      $("#img_dest").css("display", "none");
    }
  });

  $("#btn_saca_send").click(function () {
    var id = $(this).attr("value");
    var self = this;
    ajax.post("/saca/line/send/" + id, {}).then(function (result) {
      console.log(result);
    });
  });

  $(".ticket_upload").change(function () {
    console.log($(this).prev("button"));
    $(this).prev("button").css("display", "block");
  });

  $("#upload_img").click(function () {
    var fileInput = $(this).next("input");
    var saca_line_id = $("#current_saca_line").val();
    var data = {
      image_field: $(fileInput).attr("name"),
    };
    $.each(fileInput, function (outer_index, input) {
      $.each($(input).prop("files"), function (index, file) {
        data.image_file = file;
      });
    });
    ajax
      .post("/my/saca/line/" + saca_line_id + "/binary", data)
      .then(function (result) {
        console.log(result);
        window.location.href = "/my/saca/line/" + saca_line_id;
        // Location.reload();
      });
  });
});
