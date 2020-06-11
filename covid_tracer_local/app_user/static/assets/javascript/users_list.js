$(document).ready(function () {
    // Data table of users_list
    $('#users-list').DataTable({
        "pageLength": 50,
        "order": [[1, "asc"]]
    });

    // delete app_user on delete btn click
    $('.delete-btn').on('click', function(){
        choice = confirm('Are you sure!! This user will be deleted from the system');
        if ( choice=== true ){
            app_user_id = $(this).siblings('input').val();
            cur_row = $(this).closest('tr');
            rerurn_val = delete_user(app_user_id, cur_row);
        }
    })
});


function delete_user(app_user_id, cur_row){
    // delete given user from db and remove the corresponding table row from DOM
    url = '/delete_app_user/';
    $.post(url, { 'csrfmiddlewaretoken': csrf_token, 'app_user_id': app_user_id },
        function (data, status, jqXHR) {
            if (jqXHR.status == 204) {
                // remove the row from the table in DOM
                cur_row.remove();
            } else {
                alert('Could not delete user!!')
            }
        },
    ).fail(function(){
        alert('Could not delete user!!')
    });
};

