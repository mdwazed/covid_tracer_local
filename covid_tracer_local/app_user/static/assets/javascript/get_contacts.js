$(document).ready(function () {
    $('#btn-contacts').on('click', function(){
        from_date = $('#from-date').val()
        to_date = $('#to-date').val()
        app_user_id = $('#app-user-id').val()
        console.log(app_user_id);
    });
});