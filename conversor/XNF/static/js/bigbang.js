/**
 * Created by leosamu on 10/11/15.
 */
var options = ["papel", "piedra", "lagarto", "spock", "tijeras"],
  result = [" empata con ", " vence a ", " pierde contra "],
  patata = function(choice1, choice2) {
      var index1 = options.indexOf(choice1),
          index2 = options.indexOf(choice2),
          dif = index2 - index1;
      if(dif < 0) {
          dif += options.length;
      }
      while(dif > 2) {
          dif -= 2;
      }
      $("#mailto").removeClass("btn-default btn-primary btn-danger");
      switch(dif)
      {
          case 0: //empata
              $("#mailto").addClass("btn-default");
          break;
          case 1: //gana
              $("#mailto").addClass("btn-primary");
          break;
          case 2: //pierde
              $("#mailto").addClass("btn-danger");
          break;
      }

  };

  function bigBangrnd(userChoice)
  {
     var i = Math.floor(Math.random() * 5),
     randomChoice = options[i];
     $("#iagame").removeClass();
     switch(i) {
         case 0:
            $("#iagame").addClass("fa fa-hand-paper-o")
         break;
         case 1:
            $("#iagame").addClass("fa fa-hand-rock-o")
         break;
         case 2:
            $("#iagame").addClass("fa fa-hand-lizard-o")
         break;
         case 3:
            $("#iagame").addClass("fa fa-hand-spock-o")
         break;
         case 4:
            $("#iagame").addClass("fa fa-hand-scissors-o")
         break;
     }

     bigBang(userChoice,randomChoice);
  }

  function showtime()
  {
      $(".gme").removeClass("hidden");
  }