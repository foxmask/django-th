/**
 * Created by foxmask on 12/04/17.
 */
$(document).on("click","a.btn.btn-md.btn-default", function () {
    triggerId = $(this).attr('data')
    var request = $.ajax({
        url: Urls.fire_trigger(triggerId),
        type: 'get',
        dataType: 'html',
        success: showResponse,
    });
    function showResponse(response) {
        $('#trigger-footer-'+triggerId).html(response);
    }
});

$(document).on("click","a.btn.btn-md.btn-primary, a.btn.btn-md.btn-success", function () {
    triggerId = $(this).attr('data')
    var request = $.ajax({
        url: Urls.trigger_on_off(triggerId),
        type: 'get',
        dataType: 'html',
        success: showResponse,
    });
    function showResponse(response) {
        $('#trigger-record-'+triggerId).html(response);
    }
});
