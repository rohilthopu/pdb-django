function switchJP() {

    document.getElementById('na').style.display = 'none';
    document.getElementById('jp').style.display = '';
    document.getElementById('natab').classList.remove('is-active');
    document.getElementById('jptab').classList.add('is-active');

}

function switchNA() {

    document.getElementById('jp').style.display = 'none';
    document.getElementById('na').style.display = '';
    document.getElementById('jptab').classList.remove('is-active');
    document.getElementById('natab').classList.add('is-active');

}




