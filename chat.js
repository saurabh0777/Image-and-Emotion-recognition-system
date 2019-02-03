(function () {
    var Message;
    Message = function (arg) {
        this.text = arg.text, this.message_side = arg.message_side;
        this.draw = function (_this) {
            return function () {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        return this;
    };
    $(function () {
        var getMessageText, message_side, sendMessage;
        message_side = 'right';
        getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        sendMessage = function (text) {
            var $messages, message;
            if (text.trim() === '') {
                return;
            }
            $('.message_input').val('');
            $messages = $('.messages');
            message_side = message_side === 'left' ? 'right' : 'left';
            message = new Message({
                text: text,
                message_side: message_side
            });
            message.draw();
            return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
        };
        $('.send_message').click(function (e) {
        sendtochat(getMessageText())
            return sendMessage(getMessageText());
        });
        $('.message_input').keyup(function (e) {
            if (e.which === 13) {
            sendtochat(getMessageText())
                return sendMessage(getMessageText());
            }
        });

/*function sendtochat(chattext) {
   $.ajax({
        type: "POST",
        url: '/chat',
        dataType: "json",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(chattext),
        success: function(data) {

        sendMessage(data["text"])
        },
        error: function() {
            alert('Error occured');
        }
    });

}*/

function sendtochat(chattext) {
   $.ajax({
        type: "POST",
        url: 'http://127.0.0.1:8000/todo/api/v1.0/tasks/chat',
        dataType: "jsonp",
        contentType: "application/json; charset=utf-8",
    data: JSON.stringify(chattext),
        success: function(data) {

        sendMessage(data["text"])
        },
        error: function() {
            alert('Error occured');
        }
    });

}

 sendMessage('Hello Welcome to Maxis ! <br> I am Zero.');
       /* setTimeout(function () {
            return sendMessage('Hi Sandy! How are you?');
        }, 1000);
        return setTimeout(function () {
            return sendMessage('I\'m fine, thank you!');
        }, 2000);*/
    });
}.call(this));