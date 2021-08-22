$( document ).on( 'click', '.details a', function(event) {
    if (event.target.hasAttribute('href')) {
        var link = event.target.href + '/ajax/';
        console.log(link);
            $.ajax({
                url: link,
                success: function (data) {
                    $('.details-products').html(data.result);
                },
            });
            console.log(link.split('/'));
            if (link.split('/')[4] != 'ajax') {
                event.preventDefault();
            }
        
    }
 });