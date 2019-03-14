$(function () {

    $('#child_types').click(function () {

        console.log("子类型");
        var $child_types_container = $('#child_types_container');
        $child_types_container.show();
        var $child_types = $(this);
        var $span = $child_types.find("span").find("span");
        $span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up")

        //点击左侧按钮时自动关闭右侧按钮
        var $order_rules_container = $('#order_rules_container');
        $order_rules_container.hide();
        var $order_rules = $("#order_rules");
        var $span = $order_rules.find("span").find("span");
        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })


    $("#order_rules").click(function () {

        console.log("排序规则");
        var $order_rules_container = $('#order_rules_container');
        $order_rules_container.show();
        var $order_rules = $(this);
        var $span = $order_rules.find("span").find("span");
        $span.removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up")

        //点击右侧按钮时自动关闭左侧按钮
        var $child_types_container = $("#child_types_container");
        $child_types_container.hide();
        var $child_types = $("#child_types");
        var $span = $child_types.find("span").find("span");
        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $("#child_types_container").click(function () {

        var $child_types_container = $(this);
        $child_types_container.hide();
        var $child_types = $("#child_types");
        var $span = $child_types.find("span").find("span");
        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $("#order_rules_container").click(function () {

        var $order_rules_container = $(this);
        $order_rules_container.hide();
        var $order_rules = $("#order_rules");
        var $span = $order_rules.find("span").find("span");
        $span.removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");

    })

    $('.addShopping').click(function () {
        var $add = $(this);
        var goodsid = $add.attr('goodsid');
        $.get('/axf/addtocart/', {'goodsid': goodsid}, function (data) {
            console.log(data)
            if (data['status'] === 302) {
                window.open('/axf/login/', target = "_self");
            } else if (data['status'] === 200) {
                $add.prev('span').html(data['c_goods_num']);
            }
        })
    })
})