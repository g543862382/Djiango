function submitForm() {
    var username = $('input[name=username]');
    if (username.val().trim()==''){
        username.parent().addClass('has-error');
        username.parent().next().show();
        return
    }else {
        username.parent().removeClass('has-error');
    }
    var password = $('input[name=passwd]');
    if (password.val().trim()==''){
        password.parent().addClass('has-error');
        password.parent().next().show();
        return
    }else {
        password.parent().removeClass('has-error');
    }
    $('form').submit();
}

$(function () {
    $('input').blur(function () {
        if ($(this).val().trim()==''){
            $(this).parent().addClass('has-error');
            $(this).parent.next().show();
            return
        }else {
            $(this).parent.removeClass('has-error');
            $(this).parent.next().hide();
        }
    })
})