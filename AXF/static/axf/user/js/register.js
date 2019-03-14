$(function () {
    $('#name').change(function () {
        var $name = $('#name').val().trim()
        if ($name.length){
            console.log($name)
            $.getJSON('axf/checkuser/',{'name': $name},function (data) {
                var $username_info = $('#username_info');
                if (data['status'] === 200){
                    $username_info.html("用户名可用").css("color", 'green');
                }else  if(data['status'] ===901){
                    $username_info.html("用户已存在").css('color', 'red');
                }
            })
        }
    })
})

function check_info() {
    // var $username = $("#username_input");
    //
    // var username = $username.val().trim();
    //
    // if (!username){
    //     return false
    // }
    //
    // var info_color = $("#username_info").css('color');
    //
    // console.log(info_color);
    //
    // if (info_color == 'rgb(255, 0, 0)'){
    //     return false
    // }

    var $password_input = $("#password");

    var password = $password_input.val().trim();

    console.log(password)
    $password_input.val(md5(password));
    console.log($password_input.val(md5(password)))

    return true
}

