// document.getElementById("uploadBtn").onchange = function () {
// document.getElementById("uploadFile").value = this.value;
// };

            $('#del_files').on('click', function () {
                $('#fileList').slideUp('slow').empty();
                $('#filesToUpload').empty();
                $('#del_files').fadeOut('slow');
            });


function makeFileList() {
    //get the input and UL list
    $('#fileList').empty();
    $('#fileList').fadeIn('slow');
    $('#fileList').css('margin-top', '-20px!important');
    var input = document.getElementById('filesToUpload');
    var list = document.getElementById('fileList');

    if ($('#fileList').val() == ''){
        $('#del_files').fadeOut('slow');
    }
    //empty list for now...
    if (list){
        while (list.hasChildNodes()) {
            list.removeChild(ul.firstChild);
        }

        //for every file...
        for (var x = 0; x < input.files.length; x++) {
            //add to list
            var li = document.createElement('li');
            li.innerHTML = 'Файл ' + (x + 1) + ':  ' + input.files[x].name;
            list.append(li);
            $('#del_files').fadeIn('slow');
        }
    }

}
