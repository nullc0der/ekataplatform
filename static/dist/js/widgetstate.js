  // Hide the navbar widget link
  $("#accnt").hide();
  $("#nrel").hide();
  $("#conn").hide();
  $("#profc").hide();
  function showBox(col_id, link_id) {
    var uistate = JSON.parse(get('uistate'));
    if (uistate[col_id]) {
        uistate[col_id].removed = false;
        store('uistate', JSON.stringify(uistate));
        $(link_id).hide();
    }
    $("#" + col_id).show();
  };
  $(window).load(function() {
      var uistate = JSON.parse(get('uistate'));
      $.each(uistate, function(box_col, box_state) {
          var widget = $("#" + box_col);
          $.each(box_state, function(prop, stat) {
              if (prop === 'removed') {
                  if (stat) {
                      var box = widget.children();
                      box.removeBox();
                      if (box_col === 'timerwidget') {
                          $("#nrel").show();
                      }
                      if (box_col === 'connectionwidget') {
                          $("#conn").show();
                      }
                      if (box_col === 'profilewidget') {
                          $("#profc").show();
                      }
                  }
              } else if (prop === 'collapsed') {
                  if (stat) {
                      var box = widget.children();
                      box.toggleBox();
                  }
              }
          });
      });
  })
