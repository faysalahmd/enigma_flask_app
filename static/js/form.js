$("#input_string").prop('required',true);

// Allows only Alphabets to enter.
$('#input_string').keypress(function (e) {
    var regex = new RegExp(/^[a-zA-Z]+$/);
    var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
    if (regex.test(str)) {
        return true;
    }
    else{
        e.preventDefault();
        return false;
    }
});

// Resets the plug board
$('#btn_reset').click(function(){
   $('.key').each(function(i, obj) {
      $(obj).removeClass('inactive');
      $(obj).css("background-color", '#ffffff');
      obj.dataset.mappedto = "";
   });
   $('#btn_encode').prop('disabled', false);
   $('#btn_encode').removeClass('inactive');
   $('#plugboard_data').val("");
   selectedKey = null;
   selectedColor = null;
});



// Plugboard functionality
var selectedKey = null;
var selectedColor = null;

$('.key').click(function(){
   $elem = $('#'+this.id)

   if (this.dataset.mappedto == ""){
      if (selectedKey==null){
         var randomColor = "#" + Math.floor(Math.random()*16777215).toString(16);
         selectedColor = randomColor;
         $elem.css("background-color", randomColor);
         selectedKey = this;
         $elem.addClass('inactive');
         $('#btn_encode').prop('disabled', true);
         $('#btn_encode').addClass('inactive');
      }else{
         $elem.addClass('inactive');
         $key_value = selectedKey.id[4];
         this.dataset.mappedto = $key_value;
         $elem.css("background-color", selectedColor);
         selectedKey.dataset.mappedto = this.id[4];
         $('#plugboard_data').val($('#plugboard_data').val() + " " +selectedKey.id[4]+this.id[4]);
         selectedKey = null;
         $('#btn_encode').prop('disabled', false);
         $('#btn_encode').removeClass('inactive');
      }
   }
});


// Input type change event
$('input[type=radio][name=input_format]').change(function() {
    if (this.value == 'str') {
        $("#input_string").prop('required',true);
        $("#input_image").prop('required',false);
        $('#input_string').show()
        $('#input_image').hide()
    }else if (this.value == 'img') {
       $("#input_string").prop('required',false);
        $("#input_image").prop('required',true);
        $('#input_string').hide()
        $('#input_image').show()
    }
});


// OUtput type change event
$('input[type=radio][name=enc_format]').change(function() {
    if (this.value == 'str') {
        $("#output_files").hide()
        $("#setings_image").prop('required',false);
        $("#data_image").prop('required',false);
    }else if (this.value == 'img') {
        $("#output_files").show()
        $("#setings_image").prop('required',true);
        $("#data_image").prop('required',true);
    }
});
