$('submit').click(function() {
    alert(/[a-z ]+, [a-z]{2} /.test($('input').val()));
});