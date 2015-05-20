var timer = false;
var counter = -1;
var counted = false;



function msg(str){
    document.getElementById("message").innerHTML = str;
}

function countDown(){
    document.getElementById("btn_stop").innerHTML = "Restart";
    document.getElementById("btn_stop").innerHTML = "Pause";
    document.getElementById("message").innerHTML = "Count Down Started";
    if(counter >  0.1){
        document.getElementById("counter").innerHTML = counter;
        timer = setTimeout(function(){counter = counter - 1; countDown();}, 1000);
    } else {
        document.getElementById("counter").innerHTML = 0;
        document.getElementById("btn_start").innerHTML = "Restart";
        document.getElementById("btn_stop").innerHTML = "Submit";
        msg("Countdown over");
        timer = false;
    }
}


function stop() {
    if (timer === false){
        if(counter > 0){
            document.getElementById("id_time").value = parseInt(document.getElementById("id_time").value) - counter;
        }
        else if(counter < 0){
            document.getElementById("id_time").value = 0;
        }
        document.getElementById("submit").click();
    } else{
        clearTimeout(timer);
        timer = false;
        var time_left =document.getElementById("counter").innerHTML;
        time_left = parseInt(time_left);
        if (time_left > 0) {
            msg(document.getElementById("id_time").value - time_left);
        }
        document.getElementById("btn_start").innerHTML = "Resume";
        document.getElementById("btn_stop").innerHTML = "Submit";
    }
}

function start() {
    counted = true;
    clearTimeout(timer);
    var val =document.getElementById("id_time").value;
    msg("has started");
    val = val.replace(",",".");
    if (counter > 0){
        countDown();
    } else if (isNaN(val) || val  < 0 || val==="") {
       msg("Falsche Eingabe");
    } else  {
        counter = Math.ceil(val);
        document.getElementById("id_time").value = counter;
        document.getElementById("counter").innerHTML = counter;
        msg("started");
        countDown();
    }

}


