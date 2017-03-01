/*
var canvas = ctx.canvas ;
var hRatio = canvas.width  / img.width    ;
var vRatio =  canvas.height / img.height  ;
var ratio  = Math.min ( hRatio, vRatio );
var centerShift_x = ( canvas.width - img.width*ratio ) / 2;
var centerShift_y = ( canvas.height - img.height*ratio ) / 2;
ctx.clearRect(0,0,canvas.width, canvas.height);
ctx.drawImage(img, 0,0, img.width, img.height,
              centerShift_x,centerShift_y,img.width*ratio, img.height*ratio);
*/
var avatarCanvas = document.getElementById('avatarCanvas');
var ctx = avatarCanvas.getContext('2d');
/*var painterCanvas = document.getElementById('painterCanvas');
var painterctx = painterCanvas.getContext('2d');
var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var clickColor = new Array();
var clickSize = new Array();
var paint;
var colorClicked = false;
var choosenColor = "#000";
var choosesRadius = 5;
*/
var brightness = 0;
var hue = 0;
var lastX = avatarCanvas.width/2, lastY = avatarCanvas.height/2;
var dragStart;
var dragged = false;

/*
function addClick(x, y, dragging)
{
  clickX.push(x);
  clickY.push(y);
  clickDrag.push(dragging);
  clickColor.push(choosenColor);
  clickSize.push(choosesRadius);
}
function redraw(choosenColor){
  painterctx.lineJoin = "round";

  for(var i=0; i < clickX.length; i++) {
    painterctx.beginPath();
    if(clickDrag[i] && i){
      painterctx.moveTo(clickX[i-1], clickY[i-1]);
     }else{
       painterctx.moveTo(clickX[i]-1, clickY[i]);
     }
     painterctx.lineTo(clickX[i], clickY[i]);
     painterctx.closePath();
     painterctx.strokeStyle = clickColor[i];
     painterctx.lineWidth = clickSize[i];
     painterctx.stroke();
  }
}*/
function build_img_from_file(files) {
   if(files && files.length){
       var file = files[0];
       var reader = new FileReader();
       reader.onload = function(e) {
           updateCanvas(e.target.result);
       };
       reader.readAsDataURL(file);
   }
}
function updateCanvas(datasrc) {
    img = new Image();
    img.src = datasrc;
    img.onload = function() {
        $("#avatarCanvas").removeAttr('data-caman-id');
        var canvas = ctx.canvas;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, canvas.width, canvas.height);
    };
}
function isCanvasBlank(canvas) {
    var blank = document.createElement('canvas');
    blank.width = canvas.width;
    blank.height = canvas.height;

    return canvas.toDataURL() == blank.toDataURL();
}
function zoom(scale, degrees, cx, cy){
    var cx = (typeof cx === 'undefined') ? avatarCanvas.width/2 : cx;
    var cy = (typeof cy === 'undefined') ? avatarCanvas.height/2 : cy;

    ctx.clearRect(0,0,avatarCanvas.width,avatarCanvas.height);
    ctx.save();
    ctx.translate(cx,cy);
    if (degrees) {
        ctx.rotate(degrees*Math.PI/180);
    }
    ctx.scale(scale,scale);
    ctx.drawImage(img,-img.width/2,-img.height/2);
    ctx.restore();
}
function rotate(degrees, scale){
    ctx.clearRect(0,0,avatarCanvas.width,avatarCanvas.height);
    ctx.save();
    ctx.translate(avatarCanvas.width/2,avatarCanvas.height/2);
    if (scale) {
        ctx.scale(scale, scale);
    }
    ctx.rotate(degrees*Math.PI/180);
    ctx.drawImage(img,-img.width/2,-img.height/2);
    ctx.restore();
}
function getFinalImage() {
    //var tempCanvas = document.createElement('canvas');
    //var tempctx = tempCanvas.getContext('2d');
    //tempCanvas.width = avatarCanvas.width;
    //tempCanvas.height = avatarCanvas.height;
    //tempctx.drawImage(avatarCanvas, 0, 0);
    //tempctx.drawImage(painterCanvas, 0, 0);
    var mimeType = 'image/png';
    var imageData = avatarCanvas.toDataURL(mimeType);
    var byteString = atob(imageData.split(',')[1]);
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    var blob = new Blob([ab], {type: 'image/png'});
    return blob;
}
function resetUploadButton() {
    if ($(".upload_animated .text").hasClass('upload_done') || $(".upload_animated .text").hasClass('upload_error')) {
        $(".upload_animated .text").removeClass('upload_done');
        $(".upload_animated .text").removeClass('upload_error');
        $(".upload_animated .text>span").text('UPLOAD');
        $(".loading-bar").css('display', 'block');
        $("#uploadAvatar").attr('disabled', false);
        $(".upload_animated .icon>i").removeClass('fa-check');
        $(".upload_animated .icon>i").removeClass('fa-times');
        $(".upload_animated .icon>i").addClass('fa-arrow-up');
    }
}
$(".avatar_reset").hide();
$("#uploadAvatar").on('click', function () {
    if (!isCanvasBlank(avatarCanvas)) {
        $(".upload_animated .text>span").text('UPLOADING....');
        $('.loading-bar').css('display', 'all');
        var imgBlob = getFinalImage();
        var fd = new FormData();
        fd.append('avatarimage', imgBlob);
        $.ajax({
            url: $(this).data('url'),
            type: 'POST',
            data:fd,
            processData:false,
            contentType:false,
            cache:false,
            xhr: function() {
                var xhr = $.ajaxSettings.xhr();
                if (xhr.upload) {
                    xhr.upload.addEventListener('progress', function(evt) {
                        var percent = (evt.loaded / evt.total) * 100;
                        $('.loading-bar').width(percent + "%");
                    }, false);
                }
            return xhr;
            },
            success: function (data) {
                var date = new Date();
                $(".useravatar").attr('src', data + "?" + date.toString());
                $(".upload_animated .text>span").text('SUCCESS');
                $(".upload_animated .text").addClass('upload_done');
                $(".loading-bar").css('display', 'none');
                $(".loading-bar").width("0");
                $("#uploadAvatar").attr('disabled', true);
                $(".upload_animated .icon>i").removeClass('fa-arrow-up');
                $(".upload_animated .icon>i").addClass('fa-check');
                fetchTask();
            },
            error: function () {
                $(".upload_animated .text>span").text('ERROR');
                $(".upload_animated .text").addClass('upload_error');
                $(".loading-bar").css('display', 'none');
                $(".loading-bar").width("0");
                $("#uploadAvatar").attr('disabled', true);
                $(".upload_animated .icon>i").removeClass('fa-arrow-up');
                $(".upload_animated .icon>i").addClass('fa-times');
                fetchTask();
            }
        });
    }
})
$("#loadImage").on('click', function () {
    $("#avatarimage").click();
});
$("#avatarimage").on('change', function(){
    build_img_from_file(this.files);
    $("#loadImage").hide();
    $(".avatar_reset").show();
});
/*
$(".draw_color_picker").click(function(){
    if (!isCanvasBlank(avatarCanvas)) {
        colorClicked = true;
        choosenColor = $(this).data('color-value');
        $("#painterCanvas").css('pointer-events', 'all');
    }
});
$(".draw_pen_radius").click(function(){
    if (!isCanvasBlank(avatarCanvas)) {
        colorClicked = true;
        choosesRadius = $(this).data('radius');
        $("#painterCanvas").css('pointer-events', 'all');
        $('.draw_pen_radius').removeClass('draw_pen_active');
        $('.draw_eraser').removeClass('draw_pen_active');
        $(this).addClass('draw_pen_active');
    }
});
$(".draw_eraser").click(function(){
    if (!isCanvasBlank(avatarCanvas)) {
        colorClicked = true;
        choosenColor = "#ffffff"
        $("#painterCanvas").css('pointer-events', 'all');
        $(this).addClass('draw_pen_active');
    }
});
$(".clear_drawing").click(function(){
    if (!isCanvasBlank(avatarCanvas)) {
        painterctx.clearRect(0, 0, painterCanvas.width, painterCanvas.height);
        clickX = new Array();
        clickY = new Array();
        clickDrag = new Array();
        clickColor = new Array();
        clickSize = new Array();
    }
});
$('#painterCanvas').mousedown(function(e){
    if (colorClicked) {
        $("#loadImage").hide();
        var mouseX = e.pageX - $(this).offset().left;
        var mouseY = e.pageY - $(this).offset().top;

        paint = true;
        addClick(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top);
        redraw(choosenColor);
    }
});
$('#painterCanvas').mousemove(function(e){
    if(paint && colorClicked){
        $("#loadImage").hide();
        addClick(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
        redraw(choosenColor);
    }
});
$('#painterCanvas').mouseup(function(e){
    $("#loadImage").show();
    paint = false;
});
$('#painterCanvas').mouseleave(function(e){
    $("#loadImage").show();
    paint = false;
});
*/
$("#brightnessSlider").on('mouseup', function (e) {
    $(this).trigger('change');
})
$("#brightnessSlider").on('change', function () {
    var value = parseInt($(this).val());
    if (value != 0 && !isCanvasBlank(avatarCanvas)) {
        brightness = value;
        Caman('#avatarCanvas', function () {
            this.revert(false);
            this.brightness(brightness).hue(hue).render();
        });
    }
});
$("#hueSlider").on('mouseup', function (e) {
    $(this).trigger('change');
})
$("#hueSlider").on('change', function () {
    var value = parseInt($(this).val());
    if (value != 0 && !isCanvasBlank(avatarCanvas)) {
        hue = value;
        Caman('#avatarCanvas', function () {
            this.revert(false);
            this.hue(hue).brightness(brightness).render();
        });
    }
});
$("#zoomSlider").on('input', function () {
    var value = $(this).val();
    if (!isCanvasBlank(avatarCanvas)) {
        $("#avatarCanvas").removeAttr('data-caman-id');
        zoom(value, -$("#rotateSlider").val());
        /*if (value != 1) {
            //$("#painterCanvas").css('pointer-events', 'none');
        }
        else {
            var datasrc = img.src;
            updateCanvas(datasrc);
            //$("#painterCanvas").css('pointer-events', 'all');
        }*/
    }
});
$("#rotateSlider").on('input', function () {
    var value = -$(this).val();
    if (!isCanvasBlank(avatarCanvas)) {
        $("#avatarCanvas").removeAttr('data-caman-id');
        rotate(value, $("#zoomSlider").val());
    }
})
$("#avatarCanvas").mousedown(function (e) {
    lastX = e.offsetX || (e.pageX - $("#avatarCanvas").offset().left);
    lastY = e.offsetY || (e.pageY - $("#avatarCanvas").offset().top);
    dragStart = {'lastX': lastX, 'lastY': lastY };
    dragged = true;
});
$("#avatarCanvas").mousemove(function (e) {
    if (dragged) {
        lastX = e.offsetX || (e.pageX - $("#avatarCanvas").offset().left) - dragStart.lastX;
        lastY = e.offsetY || (e.pageY - $("#avatarCanvas").offset().top) - dragStart.lastY;
        dragged = true;
        zoom($("#zoomSlider").val(), lastX, lastY);
    }
});
$("#avatarCanvas").mouseup(function (e){
    dragged = false;
});
$("#avatarCanvas").mouseleave(function (e){
    dragged = false;
});
$("#imgModal").on('hide.bs.modal', function (e) {
    resetUploadButton();
});
$(".avatar_reset").on('click', function (e) {
    $("#avatarCanvas").removeAttr('data-caman-id');
    $("#loadImage").show();
    $(this).hide();
    ctx.clearRect(0,0,avatarCanvas.width,avatarCanvas.height);
    $("#rotateSlider")[0].MaterialSlider.change(0);
    $("#zoomSlider")[0].MaterialSlider.change(1.00);
    $("#brightnessSlider")[0].MaterialSlider.change(0);
    $("#hueSlider")[0].MaterialSlider.change(0);
    resetUploadButton();
})
