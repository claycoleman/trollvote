$(document).ready(function() {
    console.log(window.innerWidth);
    if (window.innerWidth < 768) {
        $('#main-nav').removeClass('navbar-fixed-top');
    } else {
        $('#main-nav').addClass('navbar-fixed-top');
        $('body').addClass('padding-at-top');
    }
});

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

$('#sec-vote-up').on('click', (function() {
    console.log('Voted up! ' + $('#sec-pk').val());
    $.ajax({
    type: 'GET',
    url: "/vote_up/",
    data: { 
        pk: $('#sec-pk').val()
    },
    error: function() { },
    success: function(data) {
        console.log(data[0])

        $('#sec-up-vote-count').text(data[0]);
        var src = $('#sec-vote-up').attr("src")
        src = src.replace(src.match(/[v]+[^_]+/), data[1]) + "-up.png";
        $('#sec-vote-up').attr("src", src);
        $('#sec-down-vote-count').text(data[2]);
        var src2 = $('#sec-vote-down').attr("src")
        src2 = src2.replace(src2.match(/[v]+[^_]+/), "vote-down.png");
        $('#sec-vote-down').attr("src", src2);
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

$('#sec-vote-down').on('click', (function() {
    console.log('Voted down! ' + $('#sec-pk').val());
    $.ajax({
    type: 'GET',
    url: "/vote_down/",
    data: { 
        pk: $('#sec-pk').val()
    },
    error: function() { },
    success: function(data) {
        console.log(data[0])

        $('#sec-down-vote-count').text(data[0]);
        var src = $('#sec-vote-down').attr("src")
        src = src.replace(src.match(/[v]+[^_]+/), data[1]) + "-down.png";
        $('#sec-vote-down').attr("src", src);
        $('#sec-up-vote-count').text(data[2]);
        var src2 = $('#sec-vote-up').attr("src")
        src2 = src2.replace(src2.match(/[v]+[^_]+/), "vote-up.png");
        $('#sec-vote-up').attr("src", src2);
    }
});

}));

$('.clickable-state').on('click', function(e) {

    var url = window.location.pathname;
    window.location.pathname = url.replace('choose-state', this.id);
});

$('.clickable-state').on('mousedown', function(e) {
    document.getElementById(e.target.id).style.fill = "rgb(140,0,0)";
});

$('.clickable-state').on('mouseover', function(e) {
    document.getElementById(e.target.id).style.fill = "rgb(0,140,149)";
    // console.log(e.target.id);
});


$('.clickable-state').on('mouseout', function(e) {
    document.getElementById(e.target.id).style.fill = "#d3d3d3";

});

$('#selecting-primary').on('change', function(e) {
    var str = window.location.pathname
    var url = str.replace(/\d+/, ""+this.options[this.selectedIndex].value);
    window.location.pathname = url
});

$('#comparing_candidates_select').on('change', function(e) {
    console.log($('#comparing_candidates_select').find('option:selected').val())
    $.ajax({
        type: "GET", 
        url: "/switch_candidates/",
        data: {
            pk: $('#comparing_candidates_select').find('option:selected').val()
        },
        error: function() { },
        success: function(data) {
            $('#sec-div').removeClass();
            $('#sec-div').addClass('col-sm-6 center ' + data[3]);
            $('#sec-name').text(data[0]);
            console.log(window.location.pathname);
            $('#sec-a').attr('href', '/candidate_detail/'+data[5]+"/")
            $('#sec-name').text(data[0]);
            $('#sec-hometown').text(data[1]);
            $('#sec-known-for').text(data[2]);
            $('#sec-image').attr('src', data[4]);
            $('#sec-pk').val(data[5]);
            $('#sec-up-vote-count').text(data[6]);
            $('#sec-down-vote-count').text(data[7]);
            // if they're in the up vote!
            if (data[8]) {
                var src = $('#sec-vote-down').attr("src")
                // set down vote button as NOT YET VOTED 
                src = src.replace(src.match(/[v]+[^_]+/), "vote-down.png");
                $('#sec-vote-down').attr("src", src);
                var src2 = $('#sec-vote-up').attr("src")
                // set up vote button as VOTED 
                src2 = src2.replace(src2.match(/[v]+[^_]+/), "voted-up.png");
                $('#sec-vote-up').attr("src", src2);
            } else if (data[9]) {
                var src = $('#sec-vote-down').attr("src")
                // set down vote button as VOTED 
                src = src.replace(src.match(/[v]+[^_]+/), "voted-down.png");
                $('#sec-vote-down').attr("src", src);
                var src2 = $('#sec-vote-up').attr("src")
                // set up vote button as NOT YET VOTED 
                src2 = src2.replace(src2.match(/[v]+[^_]+/), "vote-up.png");
                $('#sec-vote-up').attr("src", src2);
            } else { 
                // set both buttons as NOT YET VOTED
                var src = $('#sec-vote-down').attr("src")
                src = src.replace(src.match(/[v]+[^_]+/), "vote-down.png");
                $('#sec-vote-down').attr("src", src);
                var src2 = $('#sec-vote-up').attr("src")
                src2 = src2.replace(src2.match(/[v]+[^_]+/), "vote-up.png");
                $('#sec-vote-up').attr("src", src2);
            }
        }
    });
});

$('#header-links').children().hide();

$('#header-links').on('mouseleave', function(e) { 
    $('#header-links').children().fadeOut(); 
});


$('#header-links').on('mouseenter', function(e) {
    $('#header-links').children().fadeIn(); 
});



