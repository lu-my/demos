$(function () {

    $(".order").click(function () {

        var $order = $(this);

        var order_id = $order.attr("orderid");

        window.open('/axf/orderdetail/?order_id=' + order_id, target="_self");

    })

})