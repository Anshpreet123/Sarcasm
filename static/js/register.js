$("#btn-next").click(function() {
    $(".team-logos").addClass("show-logos")
});

$('#player2_name').keyup(function() {
    if ($(this).val().length)
        $('#player3').show();
    else
        $('#player3').hide();
});
$('#player3_name').keyup(function() {
    if ($(this).val().length)
        $('#player4').show();
    else
        $('#player4').hide();
});
$('#player4_name').keyup(function() {
    if ($(this).val().length)
        $('#player5').show();
    else
        $('#player5').hide();
});

const options = ["option1", "option2"];

options.forEach(option => {
    document.getElementById(option).addEventListener("click", function() {
        const pokeballs = document.getElementsByClassName("pokeball");
        for (var i = 0; i < pokeballs.length; i++) {
            pokeball = pokeballs[i];
            if (pokeball.parentNode.id != option) {
                pokeball.classList.remove("selected");
                pokeball.parentNode.classList.add("faded");
            } else {
                pokeball.classList.add("selected");
                pokeball.parentNode.classList.remove("faded");
            }
        }
        freshie_div = document.getElementById("option1")
        open_div = document.getElementById("option2")
        freshies_only = document.getElementById("freshies_only")
        open = document.getElementById("open")
        if (freshie_div.classList.contains("faded")) {
            open.checked = true
            freshies_only.checked = false
            console.log("Open")
        } else if (open_div.classList.contains("faded")) {
            freshies_only.checked = true
            open.checked = false
            console.log("Freshies only")
        } else {
            console.log("none selected")
        }

    });
});