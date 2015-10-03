$(document).ready(function() {
    $('#complete-1').click(function() {
        $('#obj_text').show();
    });

    $('#complete-0').click(function() {
        $('#obj_text').hide();
    });

    if ($('#obj_text').hasClass('has-error')) {
        $('#complete-1').prop('checked', true);
        $('#complete-0').prop('checked', false);
    }
});