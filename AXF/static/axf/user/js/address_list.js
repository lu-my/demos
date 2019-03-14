$(function () {

    $("#add_address").click(function () {
        console.log("add_address")
        var new_address = $("#new_address").val()
        console.log(new_address)
        $.getJSON("/axf/addaddress/", {"new_address": new_address}, function (data) {
            console.log(data)
            if(data["status"] === 200){
                window.location.reload()
            }
        })
    })
})