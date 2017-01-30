/**
 * Created by Родин Алексей on 02.01.2017.
 */

            $('#btn_submit_group_doc_send').on('click', function (e) {
                var message_doc_send = '';
                var email_err_doc_send = false;
                var email_err_doc_send_msg = false;
                var name_err_doc_send = false;
                var name_err_doc_send_msg = '';
                var tel_err_doc_send = false;
                var tel_err_doc_send_msg = '';
                var file_err_doc_send = false;
                var file_err_doc_send_msg = '';
                e.preventDefault();
                //валидация email
                if ($('#email_doc_send').val() != '') {
                    if (!email.test($('#email_doc_send').val())) {
                        $('#email_doc_send').addClass('invalid');
                        email_err_doc_send_msg = 'Проверьте правильность заполнения email<br/>';
                        email_err_doc_send = true;
                    }
                } else {
                    email_err_doc_send = true;
                    email_err_doc_send_msg = 'Введите свой email<br/>';
                    $('#email_doc_send').addClass('invalid');
                }
                //проверка имени
                if ($('#name_doc_send').val() == ''){
                    name_err_doc_send = true;
                    name_err_doc_send_msg = 'Введите свое имя </br>';
                    $('#name_doc_send').addClass('invalid');

                }
                //проверка телефона
                if ($('#tel_doc_send').val() == ''){
                    tel_err_doc_send = true;
                    tel_err_doc_send_msg = 'Введите свой номер телефона </br>';
                    $('#tel_doc_send').addClass('invalid');

                }else {
                    if (!tel_exp.test($('#tel_doc_send').val())) {
                        $('#tel_doc_send').addClass('invalid');
                        tel_err_doc_send_msg = 'Проверьте правильность номера телефона<br/>';
                        tel_err_doc_send = true;
                    }
                }
                //проверка файла
                if ($('#text_doc_send').val() == '' && $('#fileList li').length == 0){
                    file_err_doc_send = true;
                    file_err_doc_send_msg = 'Добавьте текст или файл';
                    $('#text_doc_send').addClass('invalid');

                }


                if(email_err_doc_send || name_err_doc_send || file_err_doc_send || tel_err_doc_send){
                    $('#message_doc_send').html('');
                    message_doc_send = name_err_doc_send_msg + email_err_doc_send_msg + tel_err_doc_send_msg + file_err_doc_send_msg;
                    showMessage_doc_send(message_doc_send);
// {#                    console.log($('#trans_from').val() + ' ' + $('#trans_to').val());#}

// {#                    $('#modalDocSend').on('shown.bs.modal', function () {#}
// {#                        $('#modalDocSend .modal-content').animate({'scrollTop': $('#message_doc_send').offset().top}, 2000)#}
// {##}
// {#                    });#}

                }else {
                    // showPreloader();
                    var formdata = new FormData($('#doc_send_form').get(0));
                    $.ajax({
                        url: "{% url 'ru:save_files_trans' %}",
                        type: 'POST',

                        data: formdata,


                        processData: false,
                        contentType: false,
                        error: function(data){
                            console.log(data);
                        },
                        success:function (data) {
                            // hidePreloader();

                            if (data == 'ok'){
                                $('.close').click();
                                    swal({
                                        title: 'Информация успешно отправлена',
                                        text: 'Спасибо за оказанное нам доверие! В ближайшее время на Вашу почту будет отправлено коммерческое предложение',
                                        type: 'success',
                                        confirmButtonText: 'Ok',
                                        closeOnConfirm: false
                                    });

// {#                                toastr.success('Заголовок', 'Текст все ок');#}
                            }else {
                                $('.close').click();

                                if (data == 'user_exists'){
                                    swal({
                                        title: 'Информация успешно отправлена',
                                        text: 'Спасибо за оказанное нам доверие! В ближайшее время на Вашу почту будет отправлено коммерческое предложение',
                                        type: 'success',
                                        confirmButtonText: 'Ok',
                                        closeOnConfirm: false
                                    },
                                    function (isConfirm) {
                                        if (isConfirm){
                                            swal({
                                                title: 'Пользователь с таким email уже зарегистрирован',
                                                text: 'Если учетная запись принадлежит Вам, Вы можете отслеживать свои заказы в личном кабинете',
                                                type: 'warning'
                                            })
                                        }
                                    });

                                }
                            }
    // {#                        alert(data);#}
                            clear_send_docs();
                        }
                    });

                }
            });
