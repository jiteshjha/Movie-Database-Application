//JQuery AJAX call to signUp function in app,py

$(function() {
    $('#btnSignUp').click(function() {

        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                 window.location.href = '/showSignin';
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
