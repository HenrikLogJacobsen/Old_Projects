//globale variabler
var ctx = document.getElementById("starfield").getContext("2d");
var reloadpurchase = document.getElementById("reloadpurchase");
var spawnpurchase = document.getElementById("spawnpurchase");
var triplepurchase = document.getElementById("triplepurchase");
var balance = document.getElementById("balance");
var Skip = {x:225,y:225,height:50,width:50,angle:90};
var kristianer = [];
var lasere = [];
var laser;
var monster;
var astroanimation;
var dangle = 0;
var pause = false;
var gameover = false;
var monsterspeed = 0.7;
var coins = 0;
var score = 0;
var dspawn = 2000;
var reloadtime = 0;
var reload = true;
var reloading;
var spawninterval;
var reloadtimer = reloadtime;
var pressed = [];

var kristian = new Image();
kristian.src = "media/kristian.png";
var skip = new Image();
skip.src = "media/skip.png";
var starfield = new Image();
starfield.src = "media/starfield.jpg";
var oof = new Audio();
oof.src = "media/oof.mp3"
oof.play();
ctx.fillStyle = "red";
ctx.font = "30px Arial";

window.onload = function (){
    draw();
    reloading = setInterval(reloadinterval,100);
}
     
animation();

spawninteval = setInterval(spawn,dspawn);


  
function draw() {
    ctx.drawImage(starfield,0,0,500,500);   
    drawskudd();
    drawkristian();
    rotateImage();
    drawtimer();
    astronautMovement()
    astromove();
    shooting();

    //Hitbox laser vs krisianer
    for (i=0; i<kristianer.length; i++) {
        for (j=0; j<lasere.length; j++) {
            if (kristianer[i].radius*Math.cos(Math.PI/180*kristianer[i].angle)+250-(kristianer[i].size/2)<lasere[j].radius*Math.cos(Math.PI/180*lasere[j].angle)+250+4 &&
                kristianer[i].radius*Math.cos(Math.PI/180*kristianer[i].angle)+250-(kristianer[i].size/2)+kristianer[i].size>lasere[j].radius*Math.cos(Math.PI/180*lasere[j].angle)+250 &&
                kristianer[i].radius*Math.sin(Math.PI/180*kristianer[i].angle)+250-(kristianer[i].size/2)<lasere[j].radius*Math.sin(Math.PI/180*lasere[j].angle)+250+4 &&
                kristianer[i].radius*Math.sin(Math.PI/180*kristianer[i].angle)+250-(kristianer[i].size/2)+kristianer[i].size>lasere[j].radius*Math.sin(Math.PI/180*lasere[j].angle)+250)
                {   
                    oof.play();
                    kristianer.splice(i,1);
                    lasere.splice(j,1);
                    
                    monsterspeed = monsterspeed*1.02;
                    dspawn = dspawn -50;
                    coins ++;
                    score ++;
                    balance.innerHTML = "Balance: "+coins;
                    clearInterval(spawninterval);
                    spawninterval = setInterval(spawn,dspawn);
                    break; 
            }
        }
    }
    //Hitbox kristianer vs canvas
    for (i=0; i<kristianer.length; i++) {
        if(kristianer[i].radius*Math.cos(Math.PI/180*kristianer[i].angle)+250<-100 || 
            kristianer[i].radius*Math.cos(Math.PI/180*kristianer[i].angle)+250>600 ||
            kristianer[i].radius*Math.sin(Math.PI/180*kristianer[i].angle)+250<-100||
            kristianer[i].radius*Math.sin(Math.PI/180*kristianer[i].angle)+250>600)
            {
            kristianer.splice(i,1)
        }
    }
    //Hitbox lasere vs canvas
    for (i=0; i<lasere.length; i++) {
        if(lasere[i].radius*Math.cos(Math.PI/180*lasere[i].angle)+250<0||
            lasere[i].radius*Math.cos(Math.PI/180*lasere[i].angle)+250>500||
            lasere[i].radius*Math.sin(Math.PI/180*lasere[i].angle)+250<0||
            lasere[i].radius*Math.sin(Math.PI/180*lasere[i].angle)+250>500) {
            lasere.splice(i,1);
        }
    }

    //Hitbox skip vs kristianer
    for (i=0; i<kristianer.length; i++) {
        if (kristianer[i].radius*Math.cos(Math.PI/180*kristianer[i].angle)+250-(kristianer[i].size/2)<Skip.x+Skip.width-15 &&
            kristianer[i].radius*Math.cos(Math.PI/180*kristianer[i].angle)+250-(kristianer[i].size/2)+kristianer[i].size>Skip.x+15 &&
            kristianer[i].radius*Math.sin(Math.PI/180*kristianer[i].angle)+250-(kristianer[i].size/2)<Skip.y+Skip.height-15 &&
            kristianer[i].radius*Math.sin(Math.PI/180*kristianer[i].angle)+250-(kristianer[i].size/2)+kristianer[i].size>Skip.y+15)
            {
                gameover = true;
        }
    }
ctx.fillStyle = "red";
ctx.fillText("Score: "+score,10,35);
}

function animation() { 
    draw();
    for (i=0; i<lasere.length; i++) {
        lasere[i].radius+=3;
    }
    for (i=0; i<kristianer.length; i++) {
        kristianer[i].radius = kristianer[i].radius - kristianer[i].speed;
    }
    if (!pause && !gameover)  {
        requestAnimationFrame(animation);
    }
    else if (pause) {
        ctx.font = "70px Arial";
        ctx.fillText("Game Paused",35,200);
        ctx.font = "30px Arial";
        clearInterval(spawninterval);
    }
    else {
        ctx.font = "80px Arial";
        ctx.fillText("Game Over",50,250);
    }  
}

function rotateImage() {
    ctx.save();
    ctx.translate(250, 250);
    ctx.rotate(Math.PI/180*Skip.angle);
    ctx.translate(-250, -250);
    ctx.drawImage(skip,Skip.x,Skip.y,Skip.width,Skip.height);
    ctx.restore();
}

function drawskudd() {
    for (i=0; i<lasere.length; i++) {
        ctx.save();
        ctx.translate(lasere[i].radius*Math.cos(Math.PI/180*lasere[i].angle)+250,lasere[i].radius*Math.sin(Math.PI/180*lasere[i].angle)+250);
        ctx.rotate(Math.PI/180*lasere[i].angle);
        ctx.translate(-(lasere[i].radius*Math.cos(Math.PI/180*lasere[i].angle)+250),-(lasere[i].radius*Math.sin(Math.PI/180*lasere[i].angle)+250));
        ctx.fillRect(lasere[i].radius*Math.cos(Math.PI/180*lasere[i].angle)+250,lasere[i].radius*Math.sin(Math.PI/180*lasere[i].angle)+250,10,2);
        ctx.restore(); 
    }
}

function Skudd(angle) {
    this.angle = angle-90;
    this.radius = Skip.height-20;
}

function shoot() {
    laser = new Skudd(Skip.angle);
    lasere.push(laser);
}

function astromove () {
    Skip.angle += dangle;
}

function Kristian (angle, speed, size) {
    this.angle = angle;
    this.speed = speed;
    this.radius = 300;
    this.size = size;
}

function spawn() {
    monster = new Kristian(Math.random() * 360,monsterspeed,50);
    kristianer.push(monster);
}

function drawkristian () {
    for (i=0; i<kristianer.length; i++) {
        ctx.drawImage(kristian,kristianer[i].radius*Math.cos(Math.PI/180*kristianer[i].angle)+250-(kristianer[i].size/2),kristianer[i].radius*Math.sin(Math.PI/180*kristianer[i].angle)+250-(kristianer[i].size/2),kristianer[i].size,kristianer[i].size);
    }      
}

function reloadinterval () {
    if(!reload && reloadtimer>0) {
        reloadtimer--;
    }
    else {
        reload = true;
        reloadtimer = reloadtime;   
    }
}

function drawtimer () {
    if (reloadtimer == reloadtime){
        ctx.fillStyle = "green";
        ctx.fillText("Ready",300,35);
    }
    else {
        ctx.fillText("Reloading: " + reloadtimer/10,300,35);
    }
    
}

reloadpurchase.onclick = function() {
    if (coins>=10) {
    coins = coins - 10;
    reloadtime = reloadtime - 5;
    balance.innerHTML = "Balance: "+coins;
    }
}

spawnpurchase.onclick = function () {
    if(coins>=20) {
        monsterspeed = monsterspeed*0.5;
        balance.innerHTML = "Balance: "+coins;
    }
}

triplepurchase.onclick = function () {
    if (coins>=50) {
        coins = coins - 50;
        reloadtime = 0;
        balance.innerHTML = "Balance: "+coins;
    }
}

document.onkeydown = function(event){
    if(!pressed.includes(event.keyCode)) {
        pressed.push(event.keyCode); //onkeydown event
    }
    if (event.keyCode == 13) {
        if (pause) {
            pause = false;
            animation();
        }
        else {
            pause = true;
        }
    }
    if(event.keyCode == 8){
        coins = 0;
        lasere = [];
        kristianer = [];
        monsterspeed = 1;
        dspawn = 2000;
    }
}

document.onkeyup = function(event2){
    if(pressed.includes(event2.keyCode)) //Onkeyup event
        pressed.splice(pressed.indexOf(event2.keyCode), 1)
}

function shooting() {
    if (pressed.includes(32) && reload) {          
        shoot();
        reload = false;    
    }
}

function astronautMovement(){
    if(pressed.includes(37)) {
        dangle = -4;
    } 
    else if(pressed.includes(39)){ 
        dangle = 4;
    }
    else {
        dangle = 0;
    }
}




