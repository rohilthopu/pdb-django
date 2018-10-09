function switchJP() {
    document.getElementById('na').style.display = 'none';
    document.getElementById('jp').style.display = "";
    document.getElementById('natab').classList.remove('is-active');
    document.getElementById('jptab').classList.add('is-active');
}

function switchNA() {
    document.getElementById('jp').style.display = 'none';
    document.getElementById('na').style.display = '';
    document.getElementById('jptab').classList.remove('is-active');
    document.getElementById('natab').classList.add('is-active');
}


function getGroup() {
    var userid = document.getElementById("userid").value;
    if (userid.length >= 3 && userid.length <= 11) {
        var thirdVal = parseInt(userid.charAt(2));
        if(thirdVal == 0 || thirdVal == 5) {
            document.getElementById("groupOut").innerText = "Group A";
        }
        else if(thirdVal == 1 || thirdVal == 6) {
            document.getElementById("groupOut").innerText = "Group B";
        }
        else if(thirdVal == 2 || thirdVal == 7) {
            document.getElementById("groupOut").innerText = "Group C";
        }
        else if(thirdVal == 3 || thirdVal == 8) {
            document.getElementById("groupOut").innerText = "Group D";
        }
        else if(thirdVal == 4 || thirdVal == 9) {
            document.getElementById("groupOut").innerText = "Group E";
        }
    }
    else if (userid.length >= 12) {
        document.getElementById("groupOut").innerText = "You have entered an invalid ID";
    }
    else {
        document.getElementById("groupOut").innerText = "";
    }
}

function computeTimes() {
    var actives = document.getElementsByName('active');
    var starttimes = document.getElementsByName('starttime');
    var endtimes = document.getElementsByName('endtime');
    var mobiletimes = document.getElementsByName('time-mobile');
    var time = Date.now() / 1000;

    for (var i = 0; i < actives.length; i++) {

        var status = actives[i].innerText;

        if (status === "Upcoming") {
            var startTime = parseFloat(starttimes[i].getAttribute('value'));
            var timeDiff = (startTime - time) / 3600;
            var fmtTime = secondsToHms(timeDiff * 3600);
            if (timeDiff > 0) {
                starttimes[i].innerText = fmtTime;
                mobiletimes[i].innerText = fmtTime;
            }
            else if (timeDiff < 0) {
                starttimes[i].innerText = "";
                mobiletimes[i].innerText = "";
                actives[i].innerText = "Active";
            }
        }

        else if (status === "Active") {
            var endtime = parseFloat(endtimes[i].getAttribute('value'));
            var timeDiff = (endtime - time) / 60;
            var fmtTime = secondsToHms(timeDiff * 60)

            if (timeDiff > 0) {
                endtimes[i].innerText = fmtTime;
                mobiletimes[i].innerText = fmtTime;
            }
            else {
                actives[i].innerText = "Ended";
                endtimes[i].innerText = "";
                starttimes[i].innerText = "";
                mobiletimes[i].innerText = "";
            }
        }
    }
}

function secondsToHms(d) {
    d = Number(d);

    var h = Math.floor(d / 3600);
    var m = Math.floor(d % 3600 / 60);
    var s = Math.floor(d % 3600 % 60);

    return ('0' + h).slice(-2) + ":" + ('0' + m).slice(-2) + ":" + ('0' + s).slice(-2);
}