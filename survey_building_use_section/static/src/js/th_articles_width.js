odoo.define("survey_building_use_section.th_articles_width", function (require) {
  "use strict";

  function onWindowClicked(ev) {
    var hash = window.location.hash;

    if (hash.includes("model=survey.")) {
      var thElements = document.getElementsByTagName("th");

      for (var i = 0; i < thElements.length; i++) {
        if (thElements[i].getAttribute("data-name") === "question_article_ids") {
          thElements[i].style.width = "350px";
        } else if (thElements[i].getAttribute("data-name") === "value") {
          var sibling = thElements[i].previousElementSibling;
          while (sibling) {
            if (sibling.getAttribute("data-name") === "sequence") {
              break;
            }
            sibling = sibling.previousElementSibling;
          }

          if (sibling) {
            sibling.style.width = "33px";
            thElements[i].style.width = "200px";
          }
        }
      }
    }
  }

  window.onWindowClicked = onWindowClicked;

  window.addEventListener("click", onWindowClicked);

  function runEveryTwoSeconds() {
    setTimeout(() => {
      onWindowClicked();
      runEveryTwoSeconds();
    }, 300);
  }

  runEveryTwoSeconds();

  return {};
});
