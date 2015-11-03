$('#test-input').on('keyup', function() {
    $('#output').text('');
    $('#output').append($('#test-input').val());
});

$('#search').keyup(function() {
    console.log('Key up!');
    $('#results').text('');
    $.ajax({
    type: 'GET',
    url: "/candidate_response/",
    data: {
        search: $('#search').val(),
    },
    error: function() {
        $('#results').html('<p>An error occurred</p>');
    },
    success: function(data) {
        for (var i = 0; i < data.length; i++) {  
                $('#results').append(data[i] + "</br>");
}
    }
});

});

$('#vote-up').on('click', (function() {
    console.log('Voted up! ' + $('#pk').val());
    $.ajax({
    type: 'GET',
    url: "/vote_up/",
    data: { 
        pk: $('#pk').val()
    },
    error: function() { },
    success: function(data) {
        console.log(data[0])

        $('#up-vote-count').text(data[0]);
        var src = $('#vote-up').attr("src")
        src = src.replace(src.match(/[v]+[^_]+/), data[1]) + "-up.png";
        $('#vote-up').attr("src", src);
        $('#down-vote-count').text(data[2]);
        var src2 = $('#vote-down').attr("src")
        src2 = src2.replace(src2.match(/[v]+[^_]+/), "vote-down.png");
        $('#vote-down').attr("src", src2);
    }
});

}));


$('#vote-down').on('click', (function() {
    console.log('Voted down! ' + $('#pk').val());
    $.ajax({
    type: 'GET',
    url: "/vote_down/",
    data: { 
        pk: $('#pk').val()
    },
    error: function() { },
    success: function(data) {
        console.log(data[0])
        
        $('#down-vote-count').text(data[0]);
        var src = $('#vote-down').attr("src")
        src = src.replace(src.match(/[v]+[^_]+/), data[1]) + "-down.png";
        $('#vote-down').attr("src", src);
        $('#up-vote-count').text(data[2]);
        var src2 = $('#vote-up').attr("src")
        src2 = src2.replace(src2.match(/[v]+[^_]+/), "vote-up.png");
        $('#vote-up').attr("src", src2);
    }
});

}));

$('.clickable-state').on('click', function() {
    var url = window.location.pathname;
    window.location.pathname = url.replace('choose-state', this.id);
});

$('.clickable-state').on('mouseover', function(e) {
    document.getElementById(e.target.id).style.fill = "rgb(0,0,0)";
});

$('.clickable-state').on('mouseout', function(e) {
    document.getElementById(e.target.id).style.fill = "#d3d3d3";
});




