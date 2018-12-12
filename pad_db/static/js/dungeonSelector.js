function showDifficulty() {
    let diff = document.getElementById("diffSelector").selectedIndex;

    let columns = document.getElementsByName("drops");

    for (var i = 0; i < columns.length; i++) {
        if (columns[i].style.display == '') {
            columns[i].style.display = 'none';
            break;
        }
    }
    columns[diff].style.display = '';
}