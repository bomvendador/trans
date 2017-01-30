/**
 * Created by Родин Алексей on 02.01.2017.
 */

    function showMessage_doc_send(msg) {
        $('#message_doc_send').append(msg);
        $('#message_doc_send').addClass('err_msg');
        $('#message_doc_send').slideDown('fast');
    }
        function hideMessage_doc_send() {
        $('#message_doc_send').slideUp('fast');
        $('#email_doc_send').removeClass('invalid');
        $('#tel_doc_send').removeClass('invalid');
        $('#name_doc_send').removeClass('invalid');
        $('#text_doc_send').removeClass('invalid');
        $('#message_doc_send').html('');


    }

    function clear_send_docs() {
        $('#name_doc_send').val('');
        $('#email_doc_send').val('');
        $('#tel_doc_send').val('');
        $('#trans_from').val('-- Перевод С --');
        $('#trans_to').val('-- Перевод НА --');
        $('#text_doc_send').val('');
        $('#fileList').empty();
        $('#filesToUpload').val('');
    }

    $('#btn_doc_send_open').on('click', function (e) {

        $('#btn_doc_send').click();
    });
