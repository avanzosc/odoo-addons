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
            
            // Your custom logic here
            // For example, adjust the width of table elements
            var thElements = document.getElementsByTagName('th');
            console.log('Total th elements:', thElements.length);
            
            for (var i = 0; i < thElements.length; i++) {
                if (thElements[i].getAttribute('data-name') === "question_article_ids") {
                    var currentStyle = thElements[i].getAttribute('style');
                    thElements[i].style.width = '500px';

                    console.log('Adjusted width of question_article_ids');
                } else if (thElements[i].getAttribute('data-name') === "value") {
                    var prevSibling = thElements[i].previousElementSibling;
                    prevSibling.style.width = '33px';

                    var currentStyle = thElements[i].getAttribute('style');
                    thElements[i].style.width = '200px';
  
                    console.log('Adjusted width of value');
                }
            }
        } else {
            console.log('Hash does not contain "model=survey."');
        }

        // Your custom logic here
    }

    // Attach the onWindowClicked function to the window object to make it globally accessible
    window.onWindowClicked = onWindowClicked;

    // Add event listener to detect click events
    window.addEventListener('click', onWindowClicked);
    window.addEventListener('scroll', onWindowClicked);


    // Return an empty object as the module export
    return {};
});
