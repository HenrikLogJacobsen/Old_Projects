// ******* GLOBALS *******
var restartButton = document.getElementById("restartButton");
var footerP = document.getElementById("footerP");
var playerMessage = document.getElementById("playerMessage");
var sproutIdxInput = document.getElementById("sproutIdx");
var sproutIdxButton = document.getElementById("sproutIdxButton");
var sproutIdxDiv = document.getElementById("sproutIdxDiv");

var sproutImg = new Image;
sproutImg.src = "media/sprout.PNG";

var sproutArray = [];
var vineArray = [];
var activeVineIdx = 0;
var lastSproutIdx = -1;
var lineWidth = 10;
var playerInfo = {
    ready: false,
    playerOneTurn: true,
}
var strokeColor = "green";

var c = document.getElementById("canvas");
var ctx = c.getContext("2d")
ctx.lineCap = "round";
ctx.lineWidth = lineWidth;
ctx.strokeStyle = strokeColor;
ctx.fillStyle = "white";

// ****** APP ********

window.onload = function () {
    init();
}

// ******* CLASSES *****

class Sprout {
    constructor(x, y, connections) {
        this.x = x;
        this.y = y;
        this.connections = connections; 
        this.imgScale = .15;
    }
    draw () {
        var circleScale = .03;
        ctx.lineWidth = lineWidth/5;
        ctx.beginPath();
        if (this.connections >= 3) {
            ctx.strokeStyle = "black";
        }
        ctx.arc(this.x, this.y, sproutImg.height * (this.imgScale + circleScale) / 2, 0, 2 * Math.PI);
        ctx.fill();
        ctx.drawImage(sproutImg, this.x - (sproutImg.width * this.imgScale / 2), this.y - (sproutImg.height * this.imgScale / 2),
            sproutImg.width * this.imgScale, sproutImg.height * this.imgScale)
        ctx.stroke();
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = lineWidth;
    }
}

class Vine {
    constructor(startX, startY, byPlayerOne) {
        this.startX = startX;
        this.startY = startY;
        this.posX = [];
        this.posY = [];
        this.active = true;
        this.byPlayerOne = byPlayerOne;
    }
    addPos(x, y) {
        this.posX.push(x);
        this.posY.push(y);
    }
    draw() {
        ctx.beginPath();
        if (this.byPlayerOne) {
            ctx.strokeStyle = "blue";
        }
        else {
            ctx.strokeStyle = "red";
        }
        for (var i in this.posX ) {
            if (this.posX.length > 1 && i) {
                ctx.moveTo(this.posX[i - 1], this.posY[i - 1]);
            }
            else {
                ctx.moveTo(this.posX[i] - 1, this.posY[i]);
            }
            ctx.lineTo(this.posX[i], this.posY[i]);
        }
        ctx.stroke();
        ctx.strokeStyle = strokeColor;
    }
}

// ***** NAV & CONTROLS ****

function startGame () {
    var sproutIdx = sproutIdxInput.value
    if (sproutIdx > 0) {
       sendPlayerMessage("Player 1's turn") 
       sproutIdxDiv.style.display = "none";
       drawSprouts(sproutIdx);
       playerInfo.ready = true;
       drawCanvas();
    }
    else {
        sendPlayerMessage("Please set the amount of sprouts");
    }
}

function restartGame () {
    if(restartButton.innerHTML == "Start Game") {
        sendPlayerMessage("Please set the amount of sprouts")
    }
    else {
       sendPlayerMessage("Restarting...") 
    }
    sproutArray = [];
    vineArray = [];
    clearCanvas();
    activeVineIdx = 0;
    restartButton.innerHTML = "Restart"
    sproutIdxDiv.style.display = "block";
}

// **** EVENTS & INTERVALS

function mouseMovement (evt) {
    if (vineArray.length > 0 && vineArray[activeVineIdx].active) {
        if (vineHit(evt) >= 0) {
            failedAttempt();
        }
        else {
            vineArray[activeVineIdx].addPos(evt.layerX, evt.layerY);
            drawCanvas();
        }   
    }
    footerP.innerHTML = "("+ evt.layerX +","+ evt.layerY +")";
}

function stopDrawing (evt) {
    if (vineArray.length > 0 && vineArray[activeVineIdx].active) {
        if (avaliableSprout(evt) >= 0 && sproutArray[avaliableSprout(evt)].connections < 3) {
            vineArray[activeVineIdx].active = false;
            sproutArray[avaliableSprout(evt)].connections++;
            var newSproutIdx = Math.round(vineArray[activeVineIdx].posX.length / 2);
            var sprout = new Sprout(vineArray[activeVineIdx].posX[newSproutIdx], vineArray[activeVineIdx].posY[newSproutIdx], 2)
            sproutArray.push(sprout);
            drawCanvas();
            if (hasWon()) {
                if (playerInfo.playerOneTurn) {
                    sendPlayerMessage("Player 1 has won!");
                }
                else {
                    sendPlayerMessage("Player 2 has won!");
                }
                playerInfo.ready = false;
                playerInfo.playerOneTurn = switchTurn();
            }
            else {
                playerInfo.playerOneTurn = switchTurn();
                if (playerInfo.playerOneTurn) {
                    sendPlayerMessage("Player 1's turn");
                }
                else {
                    sendPlayerMessage("Player 2's turn");
                }
            }
        }
        else {
            failedAttempt();
        }
    }
}

function startDrawing (evt) {
    if (playerInfo.ready && avaliableSprout(evt) >= 0 && sproutArray[avaliableSprout(evt)].connections < 3) {
        lastSproutIdx = avaliableSprout(evt);
        sproutArray[lastSproutIdx].connections++;
        var vine = new Vine(evt.layerX, evt.layerY, playerInfo.playerOneTurn)
        vine.addPos(evt.layerX, evt.layerY);
        vineArray.push(vine);
        if (activeVineIdx < vineArray.length - 1) {
            activeVineIdx++;
        }
        drawCanvas();
    }
}

// **** FUNCS *****

function failedAttempt () {
    sproutArray[lastSproutIdx].connections--;
    activeVineIdx--;
    vineArray.pop();
    drawCanvas();
}

function switchTurn() {
    if (playerInfo.playerOneTurn) {
        return false;
    }
    return true;
}

function hasWon() {
    var twoLeft = 0;
    for (i in sproutArray) {
        if (sproutArray[i].connections < 2) {
            return false;
        }
        else if (sproutArray[i].connections == 2) {
            twoLeft++;
        }
    }
    if(twoLeft > 1) {
        return false;
    }
    return true;
}

function drawCanvas() {
    clearCanvas();
    for (i in vineArray) {
        vineArray[i].draw();
    }
    for (i in sproutArray) {
        sproutArray[i].draw();
    }
}

function vineHit(e) {
    for (i in vineArray) {
        if (i != activeVineIdx) {
            for (j in vineArray[i].posX) {
                if (e.layerX >= vineArray[i].posX[j] - (lineWidth / 2) &&
                e.layerX <= vineArray[i].posX[j] + (lineWidth / 2) &&
                e.layerY >= vineArray[i].posY[j] - (lineWidth / 2) &&
                e.layerY <= vineArray[i].posY[j] + (lineWidth / 2)) {
                    return i;
                }
            }
        }
    }
    return -1;
}

function avaliableSprout (e) {
    for (i in sproutArray) {
        if (e.layerX + (lineWidth / 2) >= sproutArray[i].x - (sproutImg.height * sproutArray[i].imgScale / 2) &&
            e.layerX - (lineWidth / 2) <= sproutArray[i].x + (sproutImg.height * sproutArray[i].imgScale / 2) &&
            e.layerY + (lineWidth / 2) >= sproutArray[i].y - (sproutImg.height * sproutArray[i].imgScale / 2) &&
            e.layerY - (lineWidth / 2) <= sproutArray[i].y + (sproutImg.height * sproutArray[i].imgScale / 2)) {
                return i;
        }
    }
    return -1;
}

function clearCanvas() {
    ctx.clearRect(0, 0, c.width, c.height);
}

function sendPlayerMessage (message) {
    playerMessage.innerHTML = message;
    playerMessage.classList.remove("animated");
    void playerMessage.offsetWidth;
    playerMessage.classList.add("animated");
}

function addSprout(x, y, connections) {
    var sprout = new Sprout(x, y, connections);
    sproutArray.push(sprout);
}

function drawSprouts(idx) {
    var columns = Math.ceil( Math.sqrt(idx) );
    var sproutInColumn = Math.ceil(idx / columns);
    var toDraw = idx;
    for (var i = 1; i <= columns; i++) {
        var sproutX = c.offsetWidth / columns * i - (c.offsetWidth / columns / 2);
        if ( i == columns ) {
            sproutInColumn = toDraw;
        }
        for (var j = 1; j <= sproutInColumn; j++) {
            var sproutY = c.offsetHeight / sproutInColumn * j - (c.offsetHeight / sproutInColumn / 2);  
            addSprout(sproutX, sproutY, 0)
            toDraw--;
        }
    }
}

function init () {
    c.addEventListener("mousedown", startDrawing);
    c.addEventListener("mousemove", mouseMovement);
    c.addEventListener("mouseup", stopDrawing);
    c.addEventListener("mouseleave", stopDrawing);
    
    sendPlayerMessage("Welcome to Sprout!")
    restartButton.onclick = restartGame;
    sproutIdxButton.onclick = startGame;
    
}