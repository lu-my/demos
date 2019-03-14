$(function () {
    $(".confirm").click(function () {
        console.log("confirm");
        var $confirm = $(this);
        var $li = $confirm.parents("li");
        var cartid = $li.attr("cartid");

        $.getJSON("/axf/changecartstate/", {"cartid": cartid}, function (data) {
            console.log(data);
            if (data["status"] === 200) {
                if (data["c_is_select"]) {
                    $confirm.find("span").find("span").html("√");
                } else {
                    $confirm.find("span").find("span").html("");
                    console.log("ss")
                }
                if (data['is_all_selected'] == true) {
                    $(".all_select span span").html("√");
                } else {
                    $(".all_select span span").html("");

                }
            }
        })
    })


    $(".subShopping").click(function () {

        console.log("subShopping");
        var $subShopping = $(this)
        var $li = $subShopping.parents("li")
        var cartid = $li.attr("cartid")
        console.log(cartid);

        $.getJSON("/axf/subshopping/", {"cartid": cartid}, function (data) {
            console.log(data)
            if (data["status"] === 200) {
                var $span = $subShopping.next("span")
                if (data["c_goods_num"] > 0) {
                    $span.html(data["c_goods_num"])
                } else {
                    $li.remove();
                }
            }
        })
    })

    $(".addShopping").click(function () {

        console.log("addShopping");
        var $addShopping = $(this)
        var $li = $addShopping.parents("li")
        var cartid = $li.attr("cartid")
        console.log(cartid);

        $.getJSON("/axf/addshopping/", {"cartid": cartid}, function (data) {
            console.log(data)
            if (data["status"] === 200) {
                var $span = $addShopping.prev("span")
                $span.html(data["c_goods_num"])
            }
        })
    })

    $(".all_select").click(function () {
        console.log(this)
        var $all_select = $(this);
        var select_list = [];
        var unselect_list = [];

        $(".confirm").each(function () {
            var $confirm = $(this);
            var cartid = $confirm.parents("li").attr("cartid");

            if ($confirm.find("span").find("span").html().trim()) {
                select_list.push(cartid)
            } else {
                unselect_list.push(cartid)
            }
        })

        if (unselect_list.length > 0) {
            $.getJSON("/axf/allselect/", {"cart_list": unselect_list.join("#")}, function (data) {
                console.log(data)
                if (data["status" === 200]) {
                    $(".confirm").find("span").find("span").html("√");
                    $all_select.find("span").find("span").html("√");
                }
            })
        } else {
            if (select_list.length > 0) {
                $.getJSON("/axf/allselect/", {"cart_list": select_list.join("#")}, function (data) {
                    console.log(data)
                    if (data["status" === 200]) {
                        $(".confirm").find("span").find("span").html("");
                        $all_select.find("span").find("span").html("");
                    }

                })
            }
        }

    })
    
    $("#make_order").click(function () {
        $.get("/axf/makeorder/", function (data) {
            console.log(data)
            if(data["status"] === 200){
                console.log("详情")
                window.open("/axf/orderdetail/?order_id=" + data["order_id"], target="_self");
            }
        })
    })
})