//Initial Code taken from https://codepen.io/HowToDevCode/pen/YGqgoN?editors=0010

var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var canvas1 = document.getElementById("canvas1");
var ctx1 = canvas1.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
canvas1.width = window.innerWidth;
canvas1.height = window.innerHeight;
var particles = [];
var grass_blades= [];
var num_particles = 100;
var num_blades = 70;
var counter = 0;
var counter_variant = canvas1.width/num_blades;
var colors = ["#fbcd6c","#ffe7b4","#ffebc0"];

//Helper function to get a random color - but not too dark
function GetRandomColor() {
    var i = 0;
    var color = colors[Math.floor(Math.random() * colors.length)];
    return color;
}
//Particle object with random starting position, velocity and color
var Particle = function () {
    this.x = canvas.width * Math.random();
    this.y = canvas.height * Math.random();
    this.vx = 3 * Math.random() - 2;
    this.vy = 3 * Math.random() - 2;
    this.Color = GetRandomColor();
}

var Grass = function () {
  this.base_number = counter;
  this.curve_one = Math.floor(Math.random() * 30 + 20);
  this.random_color = (Math.random() * 71) + 30;
  counter += counter_variant;

}

//Ading two methods
Particle.prototype.Draw = function (ctx) {
    ctx.fillStyle = this.Color;
    ctx.fillRect(this.x, this.y, 2, 2);
}

Grass.prototype.Draw = function (ctx1){
  
    var base_number = this.base_number;
    var curve_one = this.curve_one;
    ctx1.beginPath();
    ctx1.moveTo(base_number, canvas.height);
    ctx1.bezierCurveTo((base_number + curve_one), canvas.height, base_number, canvas.height, (base_number + 10),(canvas.height-120));
    var grass_grd = ctx1.createLinearGradient(0, canvas.height, 0, 0);
grass_grd.addColorStop(0, "black");
grass_grd.addColorStop(0.5, "rgb(2,"+this.random_color+",2)");
grass_grd.addColorStop(1, "white");
ctx1.fillStyle = grass_grd;
    ctx1.fill();
}

Particle.prototype.Update = function () {
    this.x += this.vx;
    this.y += this.vy;
 
    if (this.x<0 || this.x > canvas.width)
        this.vx = -this.vx;
 
    if (this.y < 0 || this.y > canvas.height)
        this.vy = -this.vy;
  
}


function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
   ctx1.clearRect(0, 0, canvas.width, canvas.height);

    for (var i = 0; i < num_particles; i++){
        particles[i].Update();
        particles[i].Draw(ctx);
    }
  
   for(var k = 0; k < num_particles; k++){
        grass_blades[k].Draw(ctx1);
    }
    
    requestAnimationFrame(loop);
}
//Create particles
for (var i = 0; i < num_particles; i++){
      particles.push(new Particle());
      grass_blades.push(new Grass());
}

loop();

