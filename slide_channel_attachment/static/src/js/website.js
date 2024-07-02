odoo.define("website_slide_channel_attachment.web_zip_autocomplete", function (
  require
) {
  "use strict";
  var ajax = require("web.ajax");

  $(document).ready(function () {
    $("#add_attachment_form").submit(function () {
      var input = document.getElementById("slide_attachment");
      if (!input) {
        alert("Um, couldn't find the fileinput element.");
      } else if (!input.files) {
        alert(
          "This browser doesn't seem to support the `files` property of file inputs."
        );
      } else if (!input.files[0]) {
        alert("Please select a file before clicking 'Load'");
      } else {
        var file = input.files[0];
        var fr = new FileReader();
        fr.onload = function (e) {
          // Binary data
          var file_input = e.target.result;
          var values = {
            slide_id: $("#slide_id").val(),
            attachment: file_input,
          };
          submit_file_json(values);
        };
        fr.onerror = function (e) {
          // Error occurred
          console.log("Error : " + e.type);
        };
        // Fr.readAsBinaryString(file); //as bit work with base64 for example upload to server
        fr.readAsDataURL(file);
      }
    });

    function submit_file_json(values) {
      var update_json = $.Deferred();
      update_json.resolve();

      update_json = update_json.then(function () {
        return ajax
          .jsonRpc("/slides/save_attachment", "call", values)
          .then(function (data) {
            if (!data) {
              return;
            }
          });
      });
    }
  });
});
