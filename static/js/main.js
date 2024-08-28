let clicks = 0;
let timer = 10;
let gameInterval;

function startGame() {
    clicks = 0;
    timer = 10;
    $('#timer').text(timer);
    $('#score').text('Clicks: 0');
    $('#finalScore').text('');
    $('#clickButton').prop('disabled', false);
    $('#startButton').prop('disabled', true);
    $('#nameInput').hide();

    gameInterval = setInterval(function() {
        timer--;
        $('#timer').text(timer);
        if (timer <= 0) {
            endGame();
        }
    }, 1000);
}

function endGame() {
    clearInterval(gameInterval);
    $('#clickButton').prop('disabled', true);
    $('#startButton').prop('disabled', false);
    $('#startButton').text('Restart Game');
    $('#nameInput').show();

    const clicksPerMinute = (clicks * 6).toFixed(2); // Multiply by 6 to get clicks per minute
    $('#finalScore').text(`Final Score: ${clicksPerMinute} clicks per minute`);

    // Enable submitting score
    $('#startButton').text('Submit Score').off('click').on('click', submitScore);
}

function submitScore() {
    const name = $('#nameInput').val();
    const score = parseFloat($('#finalScore').text().split(': ')[1]);
    
    if (name) {
        $.ajax({
            url: '/submit_score',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ name: name, score: score }),
            success: function(response) {
                if (response.status === 'success') {
                    alert('Score submitted successfully!');
                    updateHighScores();
                    resetGame();
                }
            },
            error: function() {
                alert('Error submitting score. Please try again.');
            }
        });
    } else {
        alert('Please enter your name before submitting.');
    }
}

function resetGame() {
    $('#startButton').text('Start Game').off('click').on('click', startGame);
    $('#nameInput').val('').hide();
}

function updateHighScores() {
    $.get('/get_high_scores', function(data) {
        const highScoresBody = $('#highScoresBody');
        highScoresBody.empty();
        data.forEach((score, index) => {
            highScoresBody.append(`
                <tr>
                    <td>${index + 1}</td>
                    <td>${score.name}</td>
                    <td>${score.score.toFixed(2)}</td>
                </tr>
            `);
        });
    });
}

$(document).ready(function() {
    $('#startButton').click(startGame);

    $('#clickButton').click(function() {
        clicks++;
        $('#score').text(`Clicks: ${clicks}`);
    });

    updateHighScores();
});
