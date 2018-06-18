function showError(msg, isUserLabel) {
    var errorP = this.parentElement.nextElementSibling;
    errorP.innerText = isUserLabel ? this.title + msg : msg;
    $(errorP).fadeIn();
    // 设置input-group 存在错误
    $(this.parentElement).addClass('has-error');

    $(this).focus(function () {
        $(errorP).fadeOut();
        $(this.parentElement).removeClass('has-error');
    });
}


$(function () {
    $('input').blur(function () {
        if (this.value.trim().length == 0) {
            showError.call(this, '不能为空',true);
            return
        }else {
            $(this).parent.removeClass('has_error');
            $(this).parent.next().fadeOut()
        }
        if (this.name == 'username' &&
            this.value.trim().length < 10) {
            showError.call(this, this.placeholder,true);
            return
        }
        if(this.name == 'nickname' &&
        this.value.trim().length > 5){
            showError.call(this,this.placeholder,true)
        }
        if (this.name == 'passwd' &&
            this.value.trim().length < 8) {
            showError.call(this, this.placeholder,true);
            return
        }
        if (this.name == 'passwd2') {
            var passwd1 = $('input[name=passwd]').val();
            if (this.value.trim() != passwd1.trim())
                showError.call(this, '两次口令不相同！',false);
            return
        }
        if (this.name == 'phone') {
            phone = this.value.trim();
            if (phone.length != 11)
                showError.call(this, '有误，请输入正确的手机号！',false);
            return
        }
            if (!/1[3-9]\d{9}/.test(phone)) {
            showError.call(this, '无效',false);
            return
        }
    });
    function submitForm() {
        var inputs = $('input');
        for(var i = 0; i<inputs; i++){
            var input = inputs.get(i);
            if($('input').val().trim() == ''){
                $(input).parent().addClass('has-error');
                $(input).parent().next().fadeIn();
                return
            }else {
                $(input).parent.removeClass('has-error');
                $(input).parent.next().fadeOut()
            }
        }
        $('form').submit(); // 提交表单
        console.log('---check regist----')
    }

})