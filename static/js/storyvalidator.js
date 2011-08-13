
$(document).ready(function(){
    var form = $("#myform");

    form.submit(function(){
        if( checkheading() && checkcontent()) return true;
        else return false;
    }); 

    function checkheading() {
        var a = $("#heading").val();
        if( a.length == 0 ) {
            $("#heading").addClass("error");
            return false;
        }else {
            $("#heading").removeClass("error");
            return true;
        }
        return false;
    }

    function checkcontent() {
        var a = $("#content").val();
        if( a.length == 0 || a.length > 500 ) {
            if( a.length == 0 ) alert("Content is empty");
            else alert("it exceeded 500 characters");
            $("#content").addClass("error");
            return false;
        }else {
            $("#content").removeClass("error");
            return true;
        }
        return false;
    }
});


