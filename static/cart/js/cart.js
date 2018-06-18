$(function () {
    // 给是否选择购买的span添加点击事件
    $('.isChose').click(function () {

        // 获取当前Element的第一个子控件
        var spanChild = $(this).children().first();
        id = spanChild.attr('id');
        if (spanChild.text().trim() == '') {
            spanChild.text('√');  //选择
        } else {
            spanChild.text(''); //取消选择
        }

        //更新后台  $.getJSON(url,function(data){})
        // 更新cart 的选择状态接口： http://127.0.0.1:8000/app/select/1
        $.getJSON('/app/select/' + id, function (data) {
            //console.log(data);  //data-->json对象
            if (data.status == 200) {
                // 选择购物车总价格Element
                var tp = $('#totalPrice').text().trim()
                //console.log('--totalPrice--',tp)
                if (data.selected) {
                    //选择
                    $('#totalPrice').text((parseFloat(tp) + parseFloat(data.price)))
                } else {
                    //取消选择
                    $('#totalPrice').text((parseFloat(tp) - parseFloat(data.price)))
                }
            }
        });
    })

    // 全部选择或取消选择

    $('#allChose').click(function () {
        var span = $(this).children().first()
        console.log()
        id = 0;
        if (span.text().trim() == '') {
            span.text('√'); // 全部选择
            $('.isChose :first-child').text('√');
            id = 0;
        } else {
            span.text(''); //取消选择
            $('.isChose :first-child').text('');
            id = 99999;
        }

        // 更新后台
        $.getJSON('/app/select/' + id, function (data) {
            // data = {status:200, price:0 }
            console.log(data);
            $('#totalPrice').text(data.price);
        });
    });

    // 添加数量

    //减少数据
    $('.subShopping').click(function () {
        cnt = $(this).next()  //获取span的Element
        if (parseInt(cnt.text()) > 0) {
            cnt.text(parseInt(cnt.text()) - 1)
            // 修改后台数据， 更新总价格
            id = this.title
            $.getJSON('/app/subCart/' + id, function (data) {
                tp = $('#totalPrice').text()
                $('#totalPrice').text(parseFloat(tp) - parseFloat(data.price))
            })
        }
    });

    $('.addShopping').click(function () {
        cnt = $(this).prev()
        console.log(cnt)
        cnt.text(parseInt(cnt.text()) + 1)
        // 修改后台数据， 更新总价格
        id = this.title
        $.getJSON('/app/addCart/' + id, function (data) {
            tp = $('#totalPrice').text()
            $('#totalPrice').text(parseFloat(tp) + parseFloat(data.price))
        })
    });
})