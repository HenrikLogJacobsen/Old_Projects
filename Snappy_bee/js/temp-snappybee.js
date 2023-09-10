var spriteSheet, loader, c, stage, canHeight, canWidth, smallestAxis;

var player = {
    playing : false,
    score : 0,
    hiscore : 0,
    dy : 0,
    alive : true
}

var sounds = {
    die: 0,
    flap: 0,
    hit: 0,
    point: 0,
    swooshing: 0
}

var fontSize = 40;
var font = "Luckiest Guy";

var firstTimeStart = true;
var firstTimeScore = true;
var firstTimeDead = true;
var firstTimePause = true;

var activeGuiElements = [];
var mainGuiElements = [];
var treeObjects = [];
var gameElements = [];
var groundTiles = [];

var activeTreeIdx = 0;

var fontSize = 0;
var outlineSize = 0;



function init() {
    
    var manifest = [
        {src: "sheet.png", id: "spritesheet"}
    ];

    for (var prop in sounds) {
        sounds[prop] = new Audio("media/sound/" + prop + ".wav");
    }
    
    loader = new createjs.LoadQueue(false);
    loader.on("complete", handleComplete);
    loader.loadManifest(manifest, true, "media/");
}

function handleComplete() {
    
    spriteSheet = new createjs.SpriteSheet({
        "images": [loader.getResult("spritesheet")],
        "framerate": 20,
        "frames": [
            [1, 1, 1850, 1250, 0, 0, -26],
            [1, 1253, 1920, 295, 0, 0, 0],
            [1853, 1, 105, 386, 0, 0, 0],
            [1853, 389, 105, 386, 0, 0, 0],
            [1853, 777, 137, 133, 0, 0, 0],
            [1853, 912, 129, 116, 0, -1, 0],
            [1853, 1030, 113, 75, 0, 0, 0],
            [1853, 1107, 71, 68, 0, 0, 0],
            [1853, 1177, 69, 68, 0, 0, 0],
            [1, 1550, 919, 465, 0, -5, -9],
            [922, 1550, 486, 378, 0, -14, -6],
            [1410, 1550, 334, 241, 0, 0, 0],
            [1410, 1793, 303, 227, 0, 0, 0],
            [1715, 1793, 302, 169, 0, 0, 0],
            [1746, 1550, 260, 113, 0, 0, 0],
            [1746, 1665, 262, 112, 0, -1, 0]
        ],
        
        "animations": {
            "bgroundnoblu": { "frames": [0] },
            "floor": { "frames": [1] },
            "tree": { "frames": [2] },
            "treedown": { "frames": [3] },
            "beetap": { "frames": [4] },
            "replay": { "frames": [5] },
            "arrow": { "frames": [6] },
            "playpausesmall": { "frames": [7] },
            "pause": { "frames": [8] },
            "title2": { "frames": [9] },
            "gameover": { "frames": [10] },
            "scoreboard": { "frames": [11] },
            "beewithhand": { "frames": [12] },
            "beeingame": { "frames": [13] },
            "startbutton": { "frames": [14] },
            "scorebutton": { "frames": [15] }
        }
    });
    initScene();
}

function initScene() {
    canvas = document.getElementById("gameCanvas");
    window.onresize = function(){ location.reload(); }
    canvas.style.backgroundColor = "#1ea1f3";

    canWidth = window.innerWidth;
    canvas.width = canWidth;
    canHeight = window.innerHeight;
    canvas.height = canHeight;
    if (canWidth > canHeight) {
        smallestAxis = "y";
        fontSize = canWidth / 25;
    }
    else {
        smallestAxis = "x";
        fontSize = canHeight / 25;
    }
    outlineSize = fontSize / 5;

    stage = new createjs.Stage(canvas);
    stage.enableMouseOver();

    c = new createjs.Container(); 
    c.cursor = "pointer"; 
    stage.addChild(c);

    bg = new createjs.Sprite(spriteSheet, "bgroundnoblu");
    scale_image(bg, smallestAxis, 1);
    bg.mouseEnabled = false;
    c.addChild(bg);

    for (i = 0; i < 4; i++) {
        ground = new createjs.Sprite(spriteSheet, "floor");
        scale_image(ground, "y", .15);
        ground.x = i * ground.getTransformedBounds().width;
        ground.y = canHeight - ground.getTransformedBounds().height;
        groundTiles.push(ground);
        ground.mouseEnabled = false;
        stage.addChild(ground);
        
    }
    bg.y = ground.y - bg.getTransformedBounds().height;
    bg.x = canWidth / 2 - (bg.getTransformedBounds().width / 2);

    titleContainer = new createjs.Container();
    
    title = new createjs.Sprite(spriteSheet, "title2");
    scale_image(title, smallestAxis, .5);

    beeMainMenu = new createjs.Sprite(spriteSheet, "beewithhand");
    scale_image(beeMainMenu, smallestAxis, .3);
    beeMainMenu.y += title.getTransformedBounds().height;
    beeMainMenu.x += beeMainMenu.getTransformedBounds().width * .6;

    titleContainer.addChild(beeMainMenu, title);
    reposition_image_center(titleContainer, .5, .37)
    titleContainer.mouseEnabled = false;
    c.addChild(titleContainer);
    activeGuiElements.push(titleContainer);

    createjs.Tween.get(titleContainer, {loop : true})
    .to({y: titleContainer.y + (canHeight * .02)}, 400, createjs.Ease.getPowInOut(2))
    .to({y: titleContainer.y}, 400, createjs.Ease.getPowInOut(2));
    
    startbutton = new createjs.Sprite(spriteSheet, "startbutton");
    scale_image(startbutton, smallestAxis, .25);
    reposition_image_center(startbutton, 1/4, .7);
    
    add_hit_area(startbutton);
    c.addChild(startbutton);
    
    activeGuiElements.push(startbutton);

    scoreButton = new createjs.Sprite(spriteSheet, "scorebutton");
    scale_image(scoreButton, smallestAxis, .25);
    reposition_image_center(scoreButton, 3/4, .7);
    add_hit_area(scoreButton);
    c.addChild(scoreButton);
    activeGuiElements.push(scoreButton);
    
    c.addEventListener("click", function(e) {
        if (typeof startbutton !== 'undefined' && e.target == startbutton) {
            startbutton.mouseEnabled = false;
            scoreButton.mouseEnabled = false;
            start_press();
        }
        else if (typeof scoreButton !== 'undefined' && e.target == scoreButton) {
            scoreButton.mouseEnabled = false;
            startbutton.mouseEnabled = false;
            score_press();
            backButton.mouseEnabled = true;
        }
        else if (typeof playButton !== 'undefined' && e.target == playButton) {
            playButton.mouseEnabled = false;
            play();
            pause_button.mouseEnabled = true;
        }
        else if (typeof pause_button !== 'undefined' && e.target == pause_button) {
            pause_button.mouseEnabled = false;
            pause();
            playButton.mouseEnabled = true;
        }
        else if (typeof replayButton !== 'undefined' && e.target == replayButton) {
            replayButton.mouseEnabled = false;
            replay();
            setTimeout(function(){startbutton.mouseEnabled = true;}, 200);
            
            scoreButton.mouseEnabled = true;
        }
        else if (typeof backButton !== 'undefined' && e.target == backButton) {
            backButton.mouseEnabled = false;
            to_main_menu();
            startbutton.mouseEnabled = true;
            scoreButton.mouseEnabled = true;
        }
    });
    
    createjs.Ticker.timingMode = createjs.Ticker.RAF;
    createjs.Ticker.addEventListener("tick", stage);

    createjs.Ticker.addEventListener("tick", handleTick);
}

function add_hit_area (image) {
    graphics = new createjs.Graphics().beginFill("#ff0000").drawRect(image.getBounds().x, image.getBounds().y, image.getBounds().width, image.getBounds().height);
    shape = new createjs.Shape(graphics);
    image.hitArea = shape;
}

function to_main_menu() {
    ease_alpha(activeGuiElements, 0, 0);
    activeGuiElements = mainGuiElements;
    ease_alpha(activeGuiElements, 300, 1);
}

function start_press() {
    sounds["swooshing"].play();
    ease_alpha(activeGuiElements, 0, 0);
    mainGuiElements = activeGuiElements;
    activeGuiElements = [];
    player.score = 0;
    setTimeout(function(){stage.addEventListener("stagemousedown", jump);}, 200);
    if (firstTimeStart) {
        firstTimeStart = false;
        

        pause_button = new createjs.Sprite(spriteSheet, "pause");
        scale_image(pause_button, smallestAxis, .15);
        reposition_image(pause_button, .05, .05);
        pause_button.alpha = 0;
        add_hit_area(pause_button);
        c.addChild(pause_button);
        
        beeTap = new createjs.Sprite(spriteSheet, "beetap");
        scale_image(beeTap, "y", .10);
        reposition_image_center(beeTap, .5, .5);
        beeTap.alpha = 0;
        stage.addChild(beeTap);

        score = new createjs.Text(player.score, fontSize * 1.4 + "px " + font, "black");
        score.outline = outlineSize;
        reposition_image_center(score, .5, .1);
        scoreFill = score.clone();
        scoreFill.outline = false;
        scoreFill.color = "white";
        stage.addChild(score, scoreFill);


        beeContainer = new createjs.Container();
        
        beeImg = new createjs.Sprite(spriteSheet, "beeingame");
        scale_image(beeImg, "y", .06);
        beeImg.x = -(beeImg.getTransformedBounds().width / 2);
        beeImg.y = -(beeImg.getTransformedBounds().height / 2);
        
        
        beeContainer.addChild(beeImg);
        beeContainer.x = canWidth / 4;
        beeContainer.y = canHeight / 2;
        beeContainer.alpha = 0;
        stage.addChild(beeContainer);
        gameElements.push(beeContainer);

        beeTween = createjs.Tween.get(beeContainer, {loop : true})
        .to({y: beeContainer.y + (canHeight * .02)}, 400, createjs.Ease.getPowInOut(2))
        .to({y: beeContainer.y}, 400, createjs.Ease.getPowInOut(2));
        
    }
    else {
        update_ingame_score([score, scoreFill]);
        beeTween.paused = false;
        beeContainer.rotation = 0;
    }
    frontElements = [pause_button, score, scoreFill, beeContainer];
    max = (canHeight - ground.getTransformedBounds().height) * 2 / 3;
    min = (canHeight - ground.getTransformedBounds().height) * 1 / 3;
    for (i = 0; i < 7; i++) {
        treeY = Math.floor(Math.random() * (max - min) ) + min;
        topTree = new createjs.Sprite(spriteSheet, "treedown");
        scale_image(topTree, "y", .6);
        topTree.x = canWidth + (topTree.getTransformedBounds().width * 3 * i);
        topTree.y = treeY - (canHeight / 9) - topTree.getTransformedBounds().height;
        topTree.mouseEnabled = false;
        c.addChild(topTree);
        

        bottomTree = new createjs.Sprite(spriteSheet, "tree");
        scale_image(bottomTree, "y", .6);
        bottomTree.x = canWidth + (bottomTree.getTransformedBounds().width * 3 * i);
        bottomTree.y = treeY + (canHeight / 9);
        bottomTree.mouseEnabled = false;
        c.addChild(bottomTree);
        treeObjects.push([topTree,bottomTree]);
        gameElements.push(topTree, bottomTree);
    }

    for (var element of frontElements) {
        c.setChildIndex(element, c.numChildren-1);
    }
    
    for (var tile of groundTiles) {
        stage.setChildIndex(tile, stage.numChildren-1);
    }
    activeGuiElements.push(pause_button, beeTap, score, scoreFill, beeContainer);

    ease_alpha(activeGuiElements, 300, 1);
    player.playing = true;
}

function pause() {
    stage.removeEventListener("stagemousedown", jump);
    createjs.Ticker.paused = true;
    pause_button.alpha = 0;
    if(firstTimePause) {
        firstTimePause = false;
        playButton = new createjs.Sprite(spriteSheet, "playpausesmall");
        scale_image(playButton, smallestAxis, .15);
        reposition_image(playButton, .05, .05);
        add_hit_area(playButton);
        c.addChild(playButton);
    }
    playButton.alpha = 1;
}

function play() {
    createjs.Ticker.paused = false;
    playButton.alpha = 0;
    pause_button.alpha = 1;
    stage.addEventListener("stagemousedown", jump);
}

function jump() {
    if (player.alive) {
        if (!beeTween.paused) {
            beeTween.paused = true;
        }
        if (player.playing) {
            sounds["flap"].play();
            beeContainer.rotation = -30;
            player.dy = -7;
        }
    }
}

function score_press() {
    sounds["swooshing"].play();
    ease_alpha(activeGuiElements, 0, 0);
    mainGuiElements = activeGuiElements;
    activeGuiElements = [];
    if (firstTimeScore) {
        firstTimeScore = false;
        
        backButton = new createjs.Sprite(spriteSheet, "arrow");
        scale_image(backButton, smallestAxis, .15);
        reposition_image_center(backButton, .12, .10);
        backButton.alpha = 0;
        add_hit_area(backButton);
        c.addChild(backButton);
        
        scoreboardContainer = new createjs.Container();
        scoreboard = new createjs.Sprite(spriteSheet, "scoreboard");

        scale_image(scoreboard, smallestAxis, .7);
        reposition_image_center(scoreboard, 1/2, 1/2);

        newestScore = new createjs.Text(player.score, fontSize + "px " + font, "black");
        newestScore.outline = outlineSize;
        reposition_image_center(newestScore, .48, 0);
        newestScore.y = scoreboard.y + (scoreboard.getTransformedBounds().height * .325);
        newestScoreFill = newestScore.clone();
        newestScoreFill.outline = false;
        newestScoreFill.color = "white";

        bestScore = new createjs.Text(player.hiscore, fontSize + "px " + font, "black");
        bestScore.outline = outlineSize;
        reposition_image_center(bestScore, .48, 0);
        bestScore.y = scoreboard.y + (scoreboard.getTransformedBounds().height * .725);
        bestScoreFill = bestScore.clone();
        bestScoreFill.outline = false;
        bestScoreFill.color = "white";

        scoreboardContainer.addChild(scoreboard, newestScore, newestScoreFill,
        bestScore, bestScoreFill);
        scoreboardContainer.mouseEnabled = false;
        scoreboardContainer.alpha = 0;
        c.addChild(scoreboardContainer);
    }
    else {
        update_score([newestScore, newestScoreFill], [bestScore, bestScoreFill]);
    }
    activeGuiElements.push(backButton);
    activeGuiElements.push(scoreboardContainer);

    ease_alpha(activeGuiElements, 300, 1);
}

function ease_alpha (elements, startIn, a) {
    for (var o of elements) {
        createjs.Tween.get(o)
        .wait(startIn)
        .to({alpha: a}, 200);
    }
}

function update_ingame_score(score) {
    for (var o of score) {
        o.text = player.score;
    }
}

function update_score (currentScore, hiscore) {
    for (var o of currentScore) {
        o.text = player.score;
    } 
    for (var o of hiscore) {
        o.text = player.hiscore;
    } 
}

function handleTick(e) {
    if (!e.paused) {
        if (player.playing && beeTween.paused) {
            beeTap.alpha = 0;
            if (player.alive) {
                playerW = beeImg.getTransformedBounds().width / 2 * .9;
                playerH = beeImg.getTransformedBounds().height / 2 * .9;
                treeW = topTree.getTransformedBounds().width;
                treeH = topTree.getTransformedBounds().height * (358 / 396);

                for (var treepair of treeObjects) {
                    if ((beeContainer.x + playerW >= treepair[0].x && 
                        beeContainer.x <= treepair[0].x + treeW &&
                        beeContainer.y - playerH <= treepair[0].y + treeH)||(
                        beeContainer.x + playerW >= treepair[1].x && 
                        beeContainer.x <= treepair[1].x + treeW &&
                        beeContainer.y + playerH >= treepair[1].y)) {
                            sounds["hit"].play();
                            player_die();
                            beeContainer.rotation = -30;
                            player.dy = -5;
                    }
                }
            }
            if (beeContainer.y + playerH > ground.y) {
                sounds["die"].play();
                player_die();
                player.playing = false;
            }
            else if (beeContainer.y < -(beeImg.getTransformedBounds().height)) {
                beeContainer.y = -(beeImg.getTransformedBounds().height - 1);
                player.dy = 0;
            }
            else {
                player.dy += .2;
                beeContainer.y += player.dy;
                beeContainer.rotation += 1.5;

                if (player.alive) {
                    max = (canHeight - ground.getTransformedBounds().height) * 2 / 3;
                    min = (canHeight - ground.getTransformedBounds().height) * 1 / 3;

                    for (i = 0; i < treeObjects.length; i++) {
                        w = treeObjects[i][0].getTransformedBounds().width;

                        isActive = is_active_tree_pair(treeObjects[i][0], i);
                        if (isActive && activeTreeIdx != i) {
                            sounds["point"].play();
                            player.score++;
                            update_ingame_score([score, scoreFill]);
                            activeTreeIdx = i;
                        }
                        
                        newY = Math.floor(Math.random() * (max - min)) + min;
                        for (var o of treeObjects[i]) {
                            o.x -= 3;
                            if (o.x <= -w) {
                                var n = i - 1;
                                if(n < 0) {
                                    n = treeObjects.length - 1;
                                }
                                treeObjects[n][0].y = newY - (canHeight / 9) - topTree.getTransformedBounds().height;
                                treeObjects[n][1].y = newY + (canHeight / 9);
                                o.x = treeObjects[n][0].x + (treeObjects[n][0].getTransformedBounds().width * 3);
                            }
                        }
                    }
                }
            }
        }
        if (player.alive) {
            for (i = 0; i < groundTiles.length; i++) {
                w = groundTiles[i].getTransformedBounds().width;
                groundTiles[i].x -= 3;
                if (groundTiles[i].x <= -w) {
                    groundTiles[i].x += w * 4;
                }
            }
        }
    }
}

function player_die() {
    pause_button.alpha = score.alpha = scoreFill.alpha = 0;
    player.alive = false;
    
    stage.removeEventListener("stagemousedown", jump);
    activeGuiElements = [];
    if (player.score > player.hiscore) {
        player.hiscore = player.score;
    }

    if (firstTimeDead) {
        firstTimeDead = false;

        gameOverImg = new createjs.Sprite(spriteSheet, "gameover");
        scale_image(gameOverImg, smallestAxis, .45);
        reposition_image_center(gameOverImg, .5, .25);
        gameOverImg.alpha = 0;
        gameOverImg.mouseEnabled = false;
        c.addChild(gameOverImg);

        replayButton = new createjs.Sprite(spriteSheet, "replay");
        scale_image(replayButton, smallestAxis, .2);
        reposition_image_center(replayButton, 1/4, 2/3);
        replayButton.alpha = 0;
        replayButton.mouseEnabled = false;
        add_hit_area(replayButton);
        c.addChild(replayButton);

        finalScoreContainer = new createjs.Container();
        finalScoreImg = new createjs.Sprite(spriteSheet, "scoreboard");

        scale_image(finalScoreImg, smallestAxis, .4);
        reposition_image_center(finalScoreImg, 2/3, 2/3);

        fractionText = .7;

        finalScore = new createjs.Text(player.score, fontSize * fractionText + "px " + font, "black");
        finalScore.outline = outlineSize * fractionText;
        reposition_image_center(finalScore, .66, 0);
        finalScore.y = finalScoreImg.y + (finalScoreImg.getTransformedBounds().height * .325);
        finalScoreFill = finalScore.clone();
        finalScoreFill.outline = false;
        finalScoreFill.color = "white";

        finalBestScore = new createjs.Text(player.hiscore, fontSize * fractionText + "px " + font, "black");
        finalBestScore.outline = outlineSize * fractionText;
        reposition_image_center(finalBestScore, .66, 0);
        finalBestScore.y = finalScoreImg.y + (finalScoreImg.getTransformedBounds().height * .7);
        finalBestScoreFill = finalBestScore.clone();
        finalBestScoreFill.outline = false;
        finalBestScoreFill.color = "white";

        finalScoreContainer.addChild(finalScoreImg, finalScore, finalScoreFill,
        finalBestScore, finalBestScoreFill);
        

        finalScoreContainer.alpha = 0;
        finalScoreContainer.mouseEnabled = false;
        c.addChild(finalScoreContainer);
        
   
    }
    else {
        update_score([finalScore, finalScoreFill], [finalBestScore, finalBestScoreFill])
    } 
    setTimeout(function(){replayButton.mouseEnabled = true;}, 200);
    frontElements = [gameOverImg, replayButton, finalScoreContainer];
    for (var element of frontElements) {
        c.setChildIndex(element, c.numChildren - 1);
    }
    activeGuiElements.push(gameOverImg, replayButton, finalScoreContainer);
    ease_alpha(activeGuiElements, 600, 1);
}

function replay(event) {
    sounds["swooshing"].play();
    replayButton.mouseEnabled = false;
    ease_alpha(activeGuiElements, 100, 0);
    gameElements[0].alpha = 0;
    ease_alpha(gameElements, 0, 0);
    activeGuiElements = mainGuiElements;
    ease_alpha(activeGuiElements, 300, 1);
    player.alive = true;
    beeContainer.rotation = 0;
    player.playing = false;
    for (var treePair of treeObjects) {
        stage.removeChild(treePair[0], treePair[1]);
    }
    treeObjects = [];
}

function is_active_tree_pair(tree, idx) {
    previousIdx = 0;
    if (idx == 0) {
        previousIdx = treeObjects.length - 1;
    }
    else {
        previousIdx = idx - 1;
    }
    if ((beeContainer.x + beeImg.getTransformedBounds().width <=
    tree.x + (tree.getTransformedBounds().width / 2)) && (
    beeContainer.x >= treeObjects[previousIdx][0].x + (treeObjects[previousIdx][0].getTransformedBounds().width / 2))) {
        return true;
    }
    return false;
}

function reposition_image (image, newX, newY) {
    image.x = newX * canWidth;
    image.y = newY * canHeight;
}

function reposition_image_center (image, newX, newY) {
    image.x = newX * canWidth - (image.getTransformedBounds().width / 2);
    image.y = newY * canHeight - (image.getTransformedBounds().height / 2);
}

function scale_image(image, scaleDir, scale) {
    if(scaleDir == "x") {
        imageWidth = image.getTransformedBounds().width;
        image.scale = scale * canWidth / imageWidth;
    }
    else if(scaleDir == "y") {
        imageHeight = image.getTransformedBounds().height;
        image.scale = scale * canHeight / imageHeight;
    }
    else {
        console.log("SCALE ERROR");
    }
}


