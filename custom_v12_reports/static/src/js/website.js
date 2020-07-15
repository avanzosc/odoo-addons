//$(document).ready(function() {
//    "use strict";
//    if (window.location.href.includes('/my/orders/'))
//    {
//        if (localStorage.getItem('report_num')) {
//            const val = localStorage.getItem('report_num');
//            localStorage.removeItem('report_num');
//            console.log('redirect + remove', val);
//            setOrderAcceptUrl(val);
//        }
//        // show modal
//        $('#modalaccept').on('show.bs.modal', function (e) {
//            const val = '&report_number=' + $('#select_coas_report_sign').val().toString();
//            localStorage.setItem('report_num', val);
//            console.log('set', val);
//         });
//        // hide modal
//        $('#modalaccept').on('hide.bs.modal', function (e) {
//              localStorage.removeItem('report_num');
//              console.log('remove', 'da igual val');
//         });
//        // change selector
//        $('#select_coas_report_sign').change(function() {
//            const val = '&report_number=' + $(this).val().toString();
//            localStorage.setItem('report_num', val);
//            console.log('set + change', val);
//        });
//    }
//
//});
//
//function setOrderAcceptUrl(val) {
//    const path = window.location.pathname + '/accept_order';
//    const search = window.location.search + val;
//    window.location.replace(path + search);
//}
// 