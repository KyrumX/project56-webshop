$(document).ready(function() {
            $("#chatbotform").submit(function(e){
                e.preventDefault(e);
                var usermessage = $('input[name="usermessage"]').val();
                var questioncase = $('input[name="case"]').val();
                $('#chatbottable').find('tbody:last-child').append(
                    '<tr><td></td><td>' + usermessage +'</td></tr>'
                );
                botResponse(usermessage, questioncase);
                $('input[name="usermessage"]').val("");
            });
        });

function sendBotMessage(usermessage, botmessage, question_case) {
    $('#chatbottable').find('tbody:last-child').append(
        '<tr><td>' + botmessage + '</td><td></td></tr>'
    );
    $('input[name="case"]').val(question_case);
    var objDiv = document.getElementById("chatbotwrap");
    objDiv.scrollTop = objDiv.scrollHeight;
}

function botResponse(usermessage, questioncase) {
    $.ajax({
        url: './GetBotResponse.py',
        async: false,
        data: {
            format: 'json',
            message: usermessage,
            questioncase: questioncase
        },
        success: function(data) {
            var response = data.response;
            var question_case = data.case;
            sendBotMessage(usermessage, response, question_case);
        },
        error: function(e) {
            return 'Sorry! Op dit moment is er een storing. Kom alstublieft later terug.'
        }
    });
}