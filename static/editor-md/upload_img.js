function initPasteDragImg(Editor) {
    var doc = document.getElementById(Editor.id)
    doc.addEventListener('paste', function (event) {
        var items = (event.clipboardData || window.clipboardData).items;
        var file = null;
        if (items && items.length) {
            // 搜索剪切板items
            for (var i = 0; i < items.length; i++) {
                if (items[i].type.indexOf('image') !== -1) {
                    file = items[i].getAsFile();
                    break;
                }
            }
        } else {
            console.log("当前浏览器不支持");
            return;
        }
        if (!file) {
            console.log("粘贴内容非图片");
            return;
        }
        uploadImg(file, Editor);
    });

    var dashboard = document.getElementById(Editor.id)
    dashboard.addEventListener("dragover", function (e) {
        e.preventDefault()
        e.stopPropagation()
    })
    dashboard.addEventListener("dragenter", function (e) {
        e.preventDefault()
        e.stopPropagation()
    })
    dashboard.addEventListener("drop", function (e) {
        e.preventDefault()
        e.stopPropagation()
        var files = this.files || e.dataTransfer.files;
        uploadImg(files[0], Editor);
    })
}

function uploadImg(file, Editor) {
    let csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    var formData = new FormData();
    var fileName = new Date().getTime() + "." + file.name.split(".").pop();
    formData.append('file', file, fileName);

    $.ajax({
        url: Editor.settings.imageUploadURL,
        type: 'post',
        data: formData,
        headers: {
            "X-CSRFToken": csrftoken,
        },
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function (msg) {

            var success = msg['code'];
            if (success === 0) {
                var url = msg["data"];
                if (/\.(png|jpg|jpeg|gif|bmp|ico)$/.test(url)) {
                    Editor.insertValue("![图片alt](" + msg["data"] + ")");
                } else {
                    Editor.insertValue("[下载附件](" + msg["data"] + ")");
                }
            } else {
                console.log(msg);
                alert("上传失败");
            }
        }
    });


}