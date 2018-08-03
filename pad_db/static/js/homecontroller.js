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