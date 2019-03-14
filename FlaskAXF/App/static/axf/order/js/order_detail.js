$(function () {

    $("#alipay").click(function () {

        console.log("支付");

        var order_id = $(this).attr("orderid");
        var total_price = $(this).attr("total_price");

        $.getJSON("/axf/alipay/", {"order_id": order_id, "subject": "test", "total_price": total_price}, function (data) {
            console.log(data);

            if(data['status'] === 200){
                window.open(data["url"]);
            }

        })
    })

})