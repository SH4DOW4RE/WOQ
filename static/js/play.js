function sub(type, answer = 0) {
    var frm = document.getElementById('form');

    switch (type) {
        case 'question':
            document.getElementById('answer').value = answer;
            frm.submit();
            break;
        case 'answer':
            document.getElementById('answer').value = "-2";
            document.getElementById('topic').value = document.getElementById('difficulty').innerHTML;
            if (document.getElementById('c').innerHTML == "Correct") {
                document.getElementById('question').value = "-10";
            } else {
                document.getElementById('question').value = "-11";
            }
            frm.submit();
            break;
        default:
            break;
    }
}

function battle() {
    var frm = document.getElementById('form');
    var q = document.getElementById('question');

    q.value = "-1";
    frm.submit();
}

function no_battle() {
    var frm = document.getElementById('form');
    var q = document.getElementById('question');
    
    q.value = "-2";
    frm.submit();
}

function die() {
    var frm = document.getElementById('form');
    var question = document.getElementById('question');

    question.value = "-5";
    frm.submit();
}

function killed() {
    var frm = document.getElementById('form');
    frm.submit();
}

function monster(type) {
    var frm = document.getElementById('form');

    switch (type) {
        case 1:
            // Goblin
            document.getElementById('attacked').value = "goblin";
            document.getElementById('question').value = "-3";
            frm.submit();
            break;
        case 2:
            // Orc
            var player = document.getElementById('player').value;
            document.getElementById('attacked').value = ("orc" + player);
            document.getElementById('question').value = "-3";
            frm.submit();
            break;
        case 3:
            // Dragon
            document.getElementById('attacked').value = "dragon";
            document.getElementById('question').value = "-3";
            frm.submit();
            break;
        default:
            break;
    }
}