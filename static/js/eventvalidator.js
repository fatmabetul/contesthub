$(document).ready(function(){
    var form = $("#eventform");
    
    form.submit(function(){
        if( !check("#datepicker") ) return false;
        if( !check("#name") ) return false;
        if( !check("#time") ) return false;
        if( !check("#loc") ) return false;
        return true;
    }); 
    
    function check( name ) {
        var a = $(name).val();
        if( a.length == 0 ) {
            $(name).addClass("error");
            return false;
        }else {
            $(name).removeClass("error");
            return true;
        }
        return false;
    }

});



