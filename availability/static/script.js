//  Warren Haskins

$(document).ready(function(){
    console.log('ready')
    $('#email').keyup(function(){
        console.log('keyup')
        var data = $('#email').serialize()
        $.ajax({
            method: 'post',
            url: '/email',
            data: data
        })
        .done(function(res){
            $('#email_message').html(res)
            console.log(res)
        })
    })
})