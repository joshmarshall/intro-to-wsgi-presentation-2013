$(function() {

  var OPEN_ATTEMPTS = 0;

  var popup = function(author) {
    console.log("POPPING UP!");
    var answer = $("<li>☑ " + author + "</li>");
    answer.hide();
    $("#quiz-answers").prepend(answer);
    answer.slideDown();
    setTimeout(function() { answer.slideUp(200, answer.remove); }, 10000);
  };

  var open = function() {
    var host = (window.location.protocol == "file:") ? "localhost" : window.location.hostname;
    host += ":8092"
    console.log("USING HOST: " + host);
    // var host = "websockets.openjosh.com";
    var socket = new WebSocket("ws://" + host + "/socket");
    socket.onopen = function() {
      console.log("CONNECTED!");
      OPEN_ATTEMPTS = 0;
    };

    var CURRENT_QUESTION = null;
    var USERS = {};

    var hide_quiz = function() {
      $("#quiz-overlay").hide();
    };

    var show_quiz = function() {
      $("#quiz-overlay").show();
    };

    var update_counts = function() {
      var attempts = CURRENT_QUESTION.data("attempts") || 0;
      var correct = CURRENT_QUESTION.data("correct") || 0;
      $("#quiz-total").text(attempts);
      $("#quiz-correct").text(correct);
    };

    var redraw = function() {
      console.log(CURRENT_QUESTION);
      if (!CURRENT_QUESTION) {
        console.log("No question!");
        hide_quiz();
        return;
      }
      show_quiz();
      $("#quiz-question").text(CURRENT_QUESTION.data("question"));
      update_counts();
    };

    var answer_correctly = function(author) {
      if (!USERS[author]) {
        USERS[author] = 0;
      }
      USERS[author] += 1;
      popup(author + ": " + USERS[author]);
      var attempts = CURRENT_QUESTION.data("attempts") || 0;
      CURRENT_QUESTION.data("attempts", parseInt(attempts) + 1);
      update_counts();
    };

    var answer_incorrectly = function(author) {
      var attempts = CURRENT_QUESTION.data("attempts") || 0;
      CURRENT_QUESTION.data("attempts", parseInt(attempts) + 1);
      update_counts();
    };

    socket.onmessage = function(data) {
      if (!CURRENT_QUESTION) {
        return;
      }
      data = JSON.parse(data.data);
      var current_answers = CURRENT_QUESTION.data("answers").split(",");
      for (var a=0; a<current_answers.length; a++) {
        var answer = (current_answers[a] + "").toLowerCase();
        if (data.text.toLowerCase().search(answer) > -1) {
          answer_correctly(data.author);
          return;
        }
      };
      answer_incorrectly(data.author);
    };

    socket.onclose = function() {
      OPEN_ATTEMPTS += 1;
      if (OPEN_ATTEMPTS >= 3) {
        console.log("TOO MANY CONNECTION FAILURES.");
        return;
      }
      console.log("CLOSED!");
      setTimeout(open, 1000);
    };

    Reveal.addEventListener('slidechanged', function(event) {
      var $slide = $(event.currentSlide);
      var $question = $slide.find(".quiz-question");
      if (!$question.length) {
        CURRENT_QUESTION = null;
      } else {
        CURRENT_QUESTION = $question;
      }
      redraw();
    });
    redraw();


  };

  open();
});
