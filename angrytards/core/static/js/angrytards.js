$(document).ready(function(){
    
    var itemTemplate = _.template($("#story-template").html());
    var commentTemplate = _.template($("#comment-template").html());

    // Templates
    var largeStoryTemplate = _.template($("#large-story-template").html());
    var mediumStoryTemplate = _.template($("#medium-story-template").html());
    var smallStoryTemplate = _.template($("#small-story-template").html());

    // Insertion point
    var app = $("#news");

    // $(".comment-url").live('click', function(e){
    //     e.preventDefault();
    //     var url = $(e.currentTarget).attr('href');
    //     $(e.currentTarget).after('<ul></ul>');
    //     $.getJSON(url, function(data){
    //         $(e.currentTarget).parent().find('ul').append(commentTemplate(data));
    //     });
    // });


    $.getJSON('/story/', gotDataCallback);

    var secondRow = {stories:[]};
    var otherRows = {stories:[]};

    function gotDataCallback(data){
        $("#loading").remove();
        for(var i = 0; i < data.length; i++){
            
            if(i === 0){
                app.append(largeStoryTemplate(data[i]));
            } else if(i > 0 && i < 4) {
                secondRow.stories.push(data[i]);
                if(secondRow.stories.length === 3){
                    app.append(mediumStoryTemplate(secondRow));
                }
            } else {
                otherRows.stories.push(data[i]);
                if(otherRows.stories.length === 4) {
                    app.append(smallStoryTemplate(otherRows));
                    otherRows.stories = [];
                }
            }


        }
    }

});