$(function () {
    $('#backBtn').click(function () {
        console.log(window.history.back())
        window.history.back()
    })
    $('#payBtnDiv > button').click(function () {
        $('#payMsg').text('使用'+$(this).text()+'正在支付')
        $('#myModal').modal({backdrop:'static', show:true});
        orderNum = $(this).parent().attr('title');
        payType = $(this).attr('title');
        $.getJSON('/app/pay/'+orderNum+'/'+payType,function (data) {
            if (data.status == 'ok'){
                $('#payMsg').text(data.msg);
                setTimeout(function () {
                    $('#myModal').modal('hide')
                    window.open('/app/cart',target = '_self')
                },3000)
            }else {
                $('#payMsg').text(data.msg);
            }
        })
    })
})