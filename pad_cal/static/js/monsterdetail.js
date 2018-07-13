function showSkill() {

    document.getElementById('monsterdata').style.display = 'none';


    document.getElementsByClassName('is-active')[0].classList.remove('is-active');
    document.getElementById('leadertab').classList.add('is-active');

    document.getElementById('leaderskill').style.display = 'block';
    document.getElementById('activeskill').style.display = 'block';

}


function showMonsterData() {

    document.getElementById('leaderskill').style.display = 'none';
    document.getElementById('activeskill').style.display = 'none';

    document.getElementsByClassName('is-active')[0].classList.remove('is-active');
    document.getElementById('monstertab').classList.add('is-active');

    document.getElementById('monsterdata').style.display = 'block';


}


