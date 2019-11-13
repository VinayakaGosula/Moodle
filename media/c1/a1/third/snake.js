var can = document.getElementById("canvas");
var cont = can.getContext("2d");

var background = new Image();
background.src = "./snimg/background.png";
var body = new Image();
body.src = "./snimg/gsq.png";

var dir;

document.body.addEventListener('keydown', function(event) 
                                       { 
            const key = event.key; 
            switch (key) { 
                case "ArrowLeft": 
                    if(dir!="r"){dir = "l";} 
                    break; 
                case "ArrowRight": 
                    if(dir!="l"){dir = "r";} 
                    break; 
                case "ArrowUp": 
                    if(dir!="d"){dir = "u";} 
                    break; 
                case "ArrowDown": 
                    if(dir!="u"){dir ="d";} 
                    break; 
            } 
        });




var u = 32;

var points = 0;
var snake=[];
snake.push([9*u,10*u]);

var eat = 0;

var xf;
var yf;

var food = new Image();
food.src = "./snimg/rsq.png";

function makeframe(){
  cont.drawImage(background,0,0,608,608);
  cont.beginPath(); 
  cont.moveTo(0,3*u);
  cont.lineTo(608,3*u);
  cont.strokeStyle = "red";
  cont.lineWidth = 3;
  cont.strokeRect(1.5,3*u,19*u-3,16*u-3);
  for(var i=0;i<snake.length;i++){
    cont.drawImage(body,snake[i][0],snake[i][1],u,u);
  }
  if(eat == 0){xf= ((Math.floor(Math.random()*17)+1)*u); yf= ((Math.floor(Math.random()*15)+3)*u); eat = 1;}
  
  var hx = snake[0][0]; var hy = snake[0][1];
  if(dir=="l"){hx = hx-u;}
  if(dir=="u"){hy = hy-u;}
  if(dir=="r"){hx = hx+u;}
  if(dir=="d"){hy = hy+u;}

  if(hx==xf && hy==yf){points++; eat =0;}
  else{snake.pop();}
  snake.unshift([hx,hy]);
  

  function bite(){
   for(var i=1;i<snake.length;i++){
     if((hx==snake[i][0])&&(hy==snake[i][1])){return true;}
     }
     return false; 
  }
  if(hx<0 || hx>18*u  || hy<3*u || hy>18*u || bite()){clearInterval(game); }
  
  
  cont.drawImage(food,xf,yf,u,u);
  cont.fillStyle = "white";
  cont.font = "45px Courier";
  cont.fillText("Score : "+points,0.2*u,2*u);

}

window.addEventListener("keydown", function(e) {
  if([37, 38, 39, 40].indexOf(e.keyCode) > -1) {
      e.preventDefault();
  }
}, false);


function reload(){location.reload();}

let game = setInterval(makeframe,125);




