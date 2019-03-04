 
// В данной функции, код который будет выполнен после полной загрузки документа
$(function(){


    // РЕГИСТРАЦИЯ

    $('#send_form').click(function(event){ 
        event.preventDefault();
        
        var first_name = $('#first_name').val();
        var username = $('#email').val();
        var password = $('#psw').val();
        var c_password = $('#confirm_psw').val();

        json_data = JSON.stringify({
            'csrfmiddlewaretoken': '{{csrf_token}}',
            'first_name': first_name,
            'username': username,
            'password': password,
            'confirm_password': c_password,
        })

        $.ajax({
            type : 'POST', 
            url  : 'http://127.0.0.1:8000/blog/signup/',
            dataType : 'json',
            data: json_data,
            contentType: "application/json",
            encode     : true,
            success: function (response) {
                if (response["password_error"] == "fail"){
                    alert("Пароли не совпадают.");
                } else {
                    alert("hello");
                    window.location.href = "/blog/";
                }; 
            }
        })
    });



    // ВХОД
    
    $('#send_login').click(function(event){ 
        event.preventDefault();

        var username = $('#email_login').val();
        var password = $('#psw_login').val();

        json_data = JSON.stringify({
            'csrfmiddlewaretoken': '{{csrf_token}}',
            'username': username,
            'password': password,
        })

        $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:8000/blog/login/',
            // data: $('#windowLogin').serialize(),
            data: json_data,
            dataType: 'json',
            contentType: "application/json",  // тип получаемого контента
            encode     : true,
            success: function (response) {
                // responce = JSON.parse(response); // equals 'Success or failed';
                if (response["status"] == "ok"){
                    window.location.href = "/blog/";
                } else{
                    window.location.href = "/blog/";
                }                                                                                                    
            }
        });
    });


    
    // ВЫХОД

    $('#logout').click(function(event){ 
        event.preventDefault();
        json_data = JSON.stringify({
            'csrfmiddlewaretoken': '{{csrf_token}}',
            'logout': "logout",
        })

        $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:8000/blog/logout/',
            data: json_data,
            dataType: 'json',
            contentType: "application/json",  // тип получаемого контента
            encode     : true,
            success: function (response) {
                if (response["status"] == "logout"){
                    window.location.href = "http://127.0.0.1:8000/blog/";
                } else{
                    // window.location.href = "/blog/#";
                    alert("Попробуйте еще раз.");
                }                                                                                                    
            }
        });
    });



    // ВЫПАДАЮЩЕЕ МЕНЮ

    $('.navbarDropdown').on('show.bs.dropdown', function () {
        $('.dropdown-menu').focus()           
    })


    // ЭФФЕКТЫ ОКНА РЕГИСТРАЦИИ И ВХОДА

    $('#regButton').click('shown.bs.modal', function() { 

        $('main').css('background-color', 'rgba(1, 1, 1, 0.75)');
        $('#windowSignup').fadeIn(500, function(){  // плавное открытие
            $('input').css('opacity', '1.1'); // анимация для input элементов
        }); 
        // $('#window').show();
    });

    $('.close').click(function() { 
        $('#windowSignup').fadeOut(500); // плавное закрытие
        //$('main').css('background-color', 'gold');
        $('#window').hide();
    });

    $('#logButton').click('shown.bs.modal', function() { 
        $('body').css('background', 'rgba(1, 1, 1, 0.75)');
        $('#windowLogin').fadeIn(500, function(){  // плавное открытие
            $('input').css('opacity', '1.1'); // анимация для input элементов
        }); 
        // $('#window').show();
    });

    $('.close').click(function() { 
        $('#windowLogin').fadeOut(500); // плавное закрытие
        //$('main').css('background-color', 'gold');
            $('#window').hide();
    });




    // $('.close').click(function() { 
    //     $('#windowRoom').fadeOut(500); // плавное закрытие
    //     $('#window').hide();
    // });




































    
    // ДЛЯ ЛИЧНЫХ СООБЩЕНИЙ

    
    
    var user_click = 0
    // var room_id = -1;

    // function() написать функцию которая переодически обновляет контент


    $('.btnq').click(function(event){ 

        $(this).parent().parent().parent().parent().next('.chatq').fadeToggle();
        $('body').css('background', 'rgba(1, 1, 1, 0.75)');
        $('.windowRoom').fadeIn(500, function(){  // плавное открытие
            $('input').css('opacity', '1.1'); // анимация для input элементов
        });  

        event.preventDefault();

        var value = $(this).val();
        var user_auth = $('.user_auth').val();
        
        user_click = value

        json_d = {
            'value': value,
            'user_auth': user_auth,
        };

        $('.layer_chat').scrollTop(100000);

        $.ajax({
            type: "GET",
            url: 'http://127.0.0.1:8000/blog/room/',
            data: json_d,
            encode: true,
            success: function (response) {

                var ports = JSON.parse(response)
                var i = 0
                while (true){
                    var user = ports[i]['fields']['user'];
                    var content = ports[i]['fields']['content'];
                    var timestamp = ports[i]['fields']['timestamp'];

                    // var dt = new Date();

                    $('.inner').append('<blockquote class="blockquote"><footer class="blockquote-footer"><small><cite title="Source Title">' + user + '</cite></small></footer><p class="mb-0"><small>' + content + '</small></p><footer class="blockquote-footer"><small><cite title="Source Title">' + timestamp + '</cite></small></footer></blockquote>'); 
                    i++;
                    $('.layer_chat').scrollTop(100000);
                }            
            },
            error: function(rs, e){
                console.log(rs.responseText);
            }
        });
    });




    
    $('.btn_mess').click(function(event){ 
        event.preventDefault();
        var value = user_click;
        var user_auth = $('.user_auth').val();
        var message = $('.msg_field').val();

        json_data = JSON.stringify({
            'csrfmiddlewaretoken': '{{csrf_token}}',
            'message': message,
            'value': value,
            'user_auth': user_auth,
        });
        
        $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:8000/blog/room/',
            data: json_data,
            dataType: 'json',
            contentType: "application/json",
            encode     : true,
            success: function (response) {

                var user = response["user"];
                var content = response["content"];
                var timestamp = response["timestamp"];
                // var dt = new Date();

                $('.inner').append('<blockquote class="blockquote"><footer class="blockquote-footer"><small><cite title="Source Title">' + user + '</cite></small></footer><p class="mb-0"><small>' + content + '</small></p><footer class="blockquote-footer"><small><cite title="Source Title">' + timestamp + '</cite></small></footer></blockquote>'); 

                $('.btn_mess').ready(function() {
                    $('.layer_chat').scrollTop(100000);
                });
            },
            error: function(rs, e){
                console.log(rs.responseText);
            }
        });      
    });
});








        

$(document).ready(function(event){

    // ОБНОВЛЕНИЕ КОНТЕНТА

    $(document).on('submit', '.chat-form', function(event){
        event.preventDefault();
        console.log($(this).serialize());
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response){
                $('.main-chat-section').html(response['form']);
                $('textarea').val('');
                $('.btn').ready(function() {
                    $('.layer').scrollTop(100000);
                });
            },
            error: function(rs, e){
                console.log(rs.responseText);
            },
        });
    });


    // СКРОЛЛ В КОНЕЦ 

    $(document).ready(function() {
        $('.layer').scrollTop(100000);
    });
   
    // ВЫПАДАНИЕ ОТВЕТОВ

    $(".reply-btn").click(function(){
        $(this).parent().parent().next('.replied-comments').fadeToggle()
    });

    // FOR COMMENTS

    $(document).on('submit', '.comment-form', function(event){
        event.preventDefault();
        console.log($(this).serialize());
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response){
                $('.main-comment-section').html(response['form']);
                $('textarea').val('');
                $('.reply-btn').click(function() {
                    $(this).parent().parent().next('.replied-comments').fadeToggle();
                    $('textarea').val('');
                });
            },
            error: function(rs, e){
                console.log(rs.responseText);
            },
        });
    });


    // FOR REPLY

    $(document).on('submit', '.reply-form', function(event){
        event.preventDefault();
        console.log($(this).serialize());
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response){
                $('.main-comment-section').html(response['form']);
                $('textarea').val('');
                $('.reply-btn').click(function() {
                    $(this).parent().parent().next('.replied-comments').fadeToggle();
                    $('textarea').val('');
                });
            },
            error: function(rs, e){
                console.log(rs.responseText);
            },
        });
    });
});

















// // КОММЕНТАРИИ

    // $('#create_comment').click(function(event){ 
    //     event.preventDefault();

    //     var comment_top = $('#comment_top').val();
    //     var comment = $('#comment').val();

    //     json_data = JSON.stringify({
    //         'csrfmiddlewaretoken': '{{csrf_token}}',
    //         'comment_top': comment_top,
    //         'comment': comment,
    //     })

    //     $.ajax({
    //         type: "POST",
    //         url: 'http://127.0.0.1:8000/blog/post/',
    //         // data: $('#windowLogin').serialize(),
    //         data: json_data,
    //         dataType: 'json',
    //         contentType: "application/json",
    //     });
    // });









    // setInterval(function() {
    //     $.ajax({
    //         type: 'POST',
    //         url: $(this).attr('action'),
    //         data: $(this).serialize(),
    //         dataType: 'json',
    //         success: function(response){
    //             $('.main-chat-section').html(response['form']);
    //             $('textarea').val('');
    //             $(document).ready(function() {
    //                 $('.layer').scrollTop(100000);
    //             });
    //         },
    //         error: function(rs, e){
    //             console.log(rs.responseText);
    //         },
    //     });
    // }, 1000);





    // function rep(){  
    //     event.preventDefault();
    //     console.log($(this).serialize());
    //     $.ajax({
    //         type: 'POST',
    //         url: $(this).attr('action'),
    //         data: $(this).serialize(),
    //         dataType: 'json',
    //         success: function(response){
    //             $('.main-chat-section').html(response['form']);
    //             $('textarea').val('');
    //             $(document).ready(function() {
    //                 $('.layer').scrollTop(100000);
    //             });
    //         },
    //         error: function(rs, e){
    //             console.log(rs.responseText);
    //         },
    //     });
    // };

    // setInterval(rep, 1000);  




    // $('#cha, #new1').hide();


    // $(".btnq").click(function(){
    //     $(this).parent().next('.chatq').fadeToggle();
    //     alert(val);
    // });









    // $(".btnq").click(function(){
    //     $(this).parent().next('.chatq').fadeToggle();
    // });
    








    // v = $("input").keyup(function () {
    //     var value = $(this).val();
    //     $("button").text(value);
    //     }).keyup();
    // alert(v)


    // $('.btnq').click(function(event){ 
    //     event.preventDefault();

    //     var value = $(this).val();

    //     json_data = JSON.stringify({
    //         'csrfmiddlewaretoken': '{{csrf_token}}',
    //         'value': "value",
    //     });

    //     console.log($(this).serialize());
    //     // var value = $(this).val();
    //     // alert(value);

    //     $.ajax({
    //         type: "POST",
    //         url: $(this).attr('action'),
    //         data: $(this).serialize(),
    //         dataType: 'json',
    //         encode     : true,
    //         success: function (response) {
    //             // var value = $(this).val();
    //             // alert(value);
    //             $(this).parent().next('.chatq').fadeToggle();                                                                                       
    //         }
    //     });
    // });

    // $(document).on('.btnq', '.room-form', function(event){
    //     event.preventDefault();
    //     console.log($(this).serialize());
    //     $.ajax({
    //         type: 'POST',
    //         url: $(this).attr('action'),
    //         data: $(this).serialize(),
    //         dataType: 'json',
    //         success: function(response){
    //             // $('.main-comment-section').html(response['form']);
    //             $('.btnq').click(function() {
    //                 var value = $(this).val();
    //                 alert(value);
    //                 $(this).parent().next('.chatq').fadeToggle();
    //             });
    //         },
    //     });
    // });


// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->



            // $(document).on('submit', '.room-form', function(event){
            //     event.preventDefault();

            //     var value = $(this).val();
            //     var user_auth = $('.user_auth').val();

            //     json_data = JSON.stringify({
            //         'csrfmiddlewaretoken': '{{csrf_token}}',
            //         // 'value': value,
            //         // 'user_auth': user_auth,
            //     });

            //     // json_d = {
            //     //     'value': value,
            //     //     'user_auth': user_auth,
            //     // };


            //     // $.ajax({
            //     //     type: "GET",
            //     //     url: 'http://127.0.0.1:8000/blog/room/',
            //     //     data: json_d,
            //     //     encode: true,
            //     //     success: function (response) {
                        
            //     //     }
            //     // });



            //     $.ajax({
            //         type: "POST",
            //         url: 'http://127.0.0.1:8000/blog/room/',
            //         data: json_data,
            //         dataType: 'json',
            //         encode     : true,
            //         success: function (response) {
            //             if (response["active_room"] == 2){
            //                 alert('hello')
            //             }

            //             $('.main-comment-section').html(response['form']);
            //             $('textarea').val('');
            //             $('.reply-btn').click(function() {
            //                 $(this).parent().parent().next('.replied-comments').fadeToggle();
            //                 $('textarea').val('');
            //             });
            //         }
            //     });
            // });







// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->
// <!-- ooooooooooooooo ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo-->


















            // $(document).on('.btnq', function(event){ 
            //     event.preventDefault();
            //     var value = $(this).val();
            //     var user_auth = $('.user_auth').val();

            //     json_data = JSON.stringify({
            //         'csrfmiddlewaretoken': '{{csrf_token}}',
            //         'value': value,
            //         'user_auth': user_auth,
            //     });

            //     // console.log($(this).serialize());
            //     json_d = {
            //         'value': value,
            //         'user_auth': user_auth,
            //     };






            //     $.ajax({
            //         type: "GET",
            //         url: 'http://127.0.0.1:8000/blog/room/',
            //         data: json_d,
            //         encode: true,
            //         success: function (response) {
            //             var rspns = response["active_room"];
            //             // $("#test3").val(rspns); 
            //             if (response["active_room"] == 2){
            //                 alert('hello');

            //             };
            //         }
            //     });

            //     $.ajax({
            //         type: "POST",
            //         url: 'http://127.0.0.1:8000/blog/room/',
            //         data: json_data,
            //         dataType: 'json',
            //         encode     : true,
            //         success: function (response) {
            //             $(".btnq").click(function(){
            //                 $(this).parent().next('.chatq').fadeToggle();
            //             });        
            //         }
            //     });
            // });
