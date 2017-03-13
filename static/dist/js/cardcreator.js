var row_html = `
<div class="card-row">
    <div class="card-col">
    </div>
</div>
`
var col_html = `
<div class="card-col">
</div>
`
var tools_overlay = `
<div class="card-tools-overlay">
    <div class="text-center">
        <button class="btn btn-rounded card-edit-text"><i class="fa fa-font"></i>Text</button>
        <button class="btn btn-rounded card-edit-image"><i class="fa fa-file-image-o"></i> Image</button>
    </div>
</div>
`
var card_div_settings = `
<div class="settings-dropdown">
    <button class="btn btn-rounded" id="cardDivSettings"><i class="fa fa-time"></i></button>
    <div class="settings-container">
        <div class="settings-height">
            <p><i class="fa fa-columns"></i> Height</p>
            <p>
                <input type="range" class="crowdfund-card-height" min="100" max="700" value="100">
            </p>
        </div>
        <div class="settings-margin">
            <p><i class="fa fa-connectdevelop"></i> Margin</p>
            <p>
                <input type="range" class="crowdfund-card-margin" min="1" max="15" value="1" tabindex="0">
            </p>
        </div>
        <div class="settings-padding">
            <p><i class="fa fa-certificate"></i> Padding</p>
            <p>
                <input type="range" class="crowdfund-card-padding" min="1" max="15" value="1" tabindex="0">
            </p>
        </div>
        <div class="settings-delete">
            <button type="button" class="crowdfund-card-remove" class="btn btn-danger btn-flat btn-block" style="padding: 10px;">
              Remove Card
            </button>
        </div>
    </div>
</div>
`
var edit_buttons = `
    <div class="settings-dropdown">
        <button class="btn btn-rounded-f btn-primary crowdfund-card-settings"><i class="fa fa-cog"></i></button>
        <div class="settings-container">
            <button class="btn btn-rounded-f btn-danger crowdfund-card-remove"><i class="fa fa-trash"></i></button>
            <button class="btn btn-rounded-f btn-warning crowdfund-card-edit"><i class="fa fa-edit"></i></button>
            <button class="btn btn-rounded-f btn-success crowdfund-card-done"><i class="fa fa-check"></i></button>
        </div>
    </div>
`
var card_div = $('.crowdfund-card-preview>.preview>.crowdfund-card');
var cardDivSelector = '.crowdfund-card-preview>.preview>.crowdfund-card ';
var last_card_col;
function uploadCardHTML() {
    $('#finalEdit').empty();
    $('#finalEdit').append($('#cardsWrapper').html());
    $("#finalEdit .crowdfund-card>.settings-dropdown").remove();
    $("#finalEdit .card-tools-overlay").remove();
    $("#finalEdit .card-col").removeAttr('contenteditable');
    console.log($('#finalEdit').html());
    $.ajax({
        url: '/en/crowdfunding/admin/update_cards_html/',
        type: 'POST',
        data: {'html': $('#finalEdit').html(), 'admin_html': $('#cardsWrapper').html()},
        success: function () {
            $('.top-right').notify({
                message: {text: 'Cards synced with server'},
                type: 'success'
            }).show();
        },
        error: function () {
            $('.top-right').notify({
                message: {text: 'There is a error in syncing card with server'},
                type: 'danger'
            }).show();
        }
    });
}
$("#cardsWrapper").sortable({
    cancel: '[contenteditable]',
    cursor: 'move',
    opacity: 0.5,
    placeholder: "ui-sortable-placeholder",
    revert: true,
    zIndex: 9999,
    helper: function(event, ui){
        var $clone =  $(ui).clone();
        $clone.css('position','absolute');
        return $clone.get(0);
    },
});
$(document).on('click', '.card-row', function () {
    $(cardDivSelector + '.card-row').removeClass('active-area');
    $(this).addClass('active-area');
    var visibleCol = $(cardDivSelector + '.card-row.active-area>.card-col').length;
    $('#colSlider')[0].MaterialSlider.change(visibleCol);
});
$("#rowSlider").on('input', function () {
    var rows = $(this).val();
    var rowHeight = 100/rows + '%';
    var visibleRow = $(cardDivSelector + '.card-row').length;
    var rowNeeded = rows - visibleRow;
    if (rowNeeded > 0) {
        card_div.append(row_html);
        $(cardDivSelector + '.card-row').css('height', rowHeight);
    }
    else {
        $(cardDivSelector + '.card-row:last').remove();
        $(cardDivSelector + '.card-row').css('height', rowHeight);
    }
});
$("#colSlider").on('input', function () {
    var cols = parseInt($(this).val());
    var colWidth = (98 / cols) + "%";
    var active_area = $(cardDivSelector + '.card-row.active-area');
    active_area.empty();
    for (var i = 0; i < cols; i++) {
        active_area.append(col_html);
    }
    $(cardDivSelector + '.card-row.active-area>.card-col').css('width', colWidth);
});
$("#paddingSlider").on('input', function () {
    var rowPadding = $(this).val() + 'px';
    var active_area = $(cardDivSelector + '.card-row.active-area');
    active_area.css('padding', rowPadding);
})
$("#doneBtn").on('click', function () {
    var cardHeight = $('#cardHeight').text();
    $("#cardsWrapper").append($('.preview').html());
    $("#cardsWrapper>.crowdfund-card:last").css('height', cardHeight);
    $("#cardsWrapper>.crowdfund-card:last .card-col").append(tools_overlay);
    $("#cardsWrapper>.crowdfund-card:last").prepend(edit_buttons);
    $("#cardCreatorModal").modal('hide');
    $("#productFeatureModal").modal('show');
});
$(document).on('click', '.crowdfund-card-settings', function () {
    $(this).siblings('.settings-container').toggleClass('show');
});
$(document).on('click', '.crowdfund-card-remove', function () {
    $(this).closest('.crowdfund-card').remove();
    uploadCardHTML();
});
$(document).on('click', '.crowdfund-card-done', function () {
    var crowdfund_card = $(this).closest('.crowdfund-card');
    crowdfund_card.find('.card-col .card-tools-overlay').remove();
    uploadCardHTML();
});
$(document).on('click', '.crowdfund-card-edit', function () {
    var crowdfund_card = $(this).closest('.crowdfund-card');
    crowdfund_card.find('.card-col').append(tools_overlay);
});
$(document).on('click', '.card-edit-text', function () {
    var card_col = $(this).closest('.card-col');
    card_col.text('Type here');
    card_col.attr('contenteditable', true);
    $(this).closest('.card-tools-overlay').remove();
});
$(document).on('click', '.card-edit-image', function () {
    last_card_col = $(this).closest('.card-col');
    $("#imageLoader").click();
})
$("#imageLoader").on('change', function () {
    last_card_col.find('.card-tools-overlay').remove();
    if(this.files && this.files.length){
        var file = this.files[0];
        var reader = new FileReader();
        reader.onload = function(e) {
            var img = new Image();
            img.src = e.target.result;
            img.onload = function () {
                last_card_col.append(img);
            }
        };
        reader.readAsDataURL(file);
    }
})
$(document).on('hidden.bs.modal', '#productFeatureModal' ,function () {
    $('html, body').animate({
        scrollTop: $("#cardsWrapper>.crowdfund-card:last").offset().top
    }, 1000);
});
$(document).on('sortupdate', '#cardsWrapper', function( event, ui ) {
    uploadCardHTML();
});
