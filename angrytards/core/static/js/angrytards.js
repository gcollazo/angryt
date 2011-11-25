$(document).ready(function(){
    
    // Share buttons
    $("#share-link").click(function(e){
        e.preventDefault();
        $(".to-hide").fadeOut('fast');
        $(this).fadeOut('fast', function(){
            $("#share-buttons").fadeIn('fast');
        });
    });

    var itemTemplate = _.template($("#story-template").html());
    var commentTemplate = _.template($("#comment-template").html());

    // Templates
    var largeStoryTemplate = _.template($("#large-story-template").html());
    var mediumStoryTemplate = _.template($("#medium-story-template").html());
    var smallStoryTemplate = _.template($("#small-story-template").html());

    // Insertion point
    var app = $("#news");

    if(app.length > 0){
        $.getJSON('/story/', gotDataCallback);
    }

    var secondRow = {stories:[]};
    var otherRows = {stories:[]};

    function gotDataCallback(data){
        $("#loading").remove();
        for(var i = 0; i < data.length; i++){
            
            if(i === 0){
                app.append(largeStoryTemplate(data[i]));
            } else if(i > 0 && i < 7) {
                secondRow.stories.push(data[i]);
                if(secondRow.stories.length === 3){
                    app.append(mediumStoryTemplate(secondRow));
                    secondRow.stories = [];
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