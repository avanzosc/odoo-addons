odoo.define('survey_building_use_section.th_articles_width', function (require) {
    'use strict';

    // Import core
    var core = require('web.core');

    // Define a translation function (_t)
    var _t = core._t;

    // Define the onWindowClicked function
    function onWindowClicked(ev) {
        console.log('Window click event occurred:', ev);

        // Check if window location hash contains 'model=survey.'
        var hash = window.location.hash;
        console.log('Hash:', hash);

        if (hash.includes('model=survey.')) {
            console.log('Hash contains "model=survey."');

            var thElements = document.getElementsByTagName('th');
            console.log('Total th elements:', thElements.length);

            for (var i = 0; i < thElements.length; i++) {
                if (thElements[i].getAttribute('data-name') === "question_article_ids") {
                    thElements[i].style.width = '350px';

                    console.log('Adjusted width of question_article_ids');
                } else if (thElements[i].getAttribute('data-name') === "value") {
                    var sibling = thElements[i].previousElementSibling;
                    while (sibling) {
                        if (sibling.getAttribute('data-name') === "sequence") {
                            // Found the sibling with data-name="sequence"
                            break;
                        }
                        sibling = sibling.previousElementSibling;
                    }

                    if (sibling) {
                        sibling.style.width = '33px';
                        thElements[i].style.width = '200px';
                        console.log('Adjusted width of value');
                    } else {
                        console.log('Sibling with data-name="sequence" not found.');
                    }
                }
            }
        } else {
            console.log('Hash does not contain "model=survey."');
        }
    }

    // Attach the onWindowClicked function to the window object to make it globally accessible
    window.onWindowClicked = onWindowClicked;

    // Add event listener to detect click events
    window.addEventListener('click', onWindowClicked);


    // Execute onWindowEvent asynchronously every 2 seconds
    function runEveryTwoSeconds() {
        setTimeout(() => {
            onWindowClicked();
            runEveryTwoSeconds(); 
        }, 2000);
    }

    runEveryTwoSeconds(); // Start the recursive function call


    // Return an empty object as the module export
    return {};
});
