let busy = false;
let busy1 = false;// чтобы не накладывать запросы друг на друга
setInterval(function() {
  if (busy) { return; }
  busy = true;
  $.ajax({
    url: 'https://youtubetreamer.onrender.com/get_board',
    type: 'get',
    success: function (response) {
       document.querySelector("#board").innerHTML = response;
       busy = false;
       $(".text").fitText();
       $(".num").fitText();
    },
    error: function (r) {
       busy = false;
    }
  });
}, 7500);

// Задаём далее код для получения quest
 setInterval(function() {
  if (busy1) { return; }
  busy1 = true;
  $.ajax({
    url: 'https://youtubetreamer.onrender.com/get_question',
    type: 'get',
    success: function (response) {
       document.querySelector(".letter-row").innerHTML = response;
       busy1 = false;
    },
    error: function (r) {
       busy1 = false;
    }
  });
}, 9000); 

$(".text").fitText();
$(".num").fitText();