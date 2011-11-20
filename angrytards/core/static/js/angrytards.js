$(document).ready(function(){
    
    var itemTemplate = _.template($("#story-template").html());
    var commentTemplate = _.template($("#comment-template").html());

    $(".comment-url").live('click', function(e){
        e.preventDefault();
        var url = $(e.currentTarget).attr('href');
        $(e.currentTarget).after('<ul></ul>');
        $.getJSON(url, function(data){
            $(e.currentTarget).parent().find('ul').append(commentTemplate(data));
        });
    });


    $.getJSON('/story/', function(data) {
        for(var i=0; i<data.length; i++){
            $("#app").append(itemTemplate(data[i]));
        }
    });

});