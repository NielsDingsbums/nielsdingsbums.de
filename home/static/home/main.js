var colors = ["#22a6b3", "#6ab04c", "#eb4d4b", "#f0932b", "#95afc0"];
var words = ["programmiere", "entwickle", "bastle", "tue", "erschaffe", "zerstöre"];

var i = 0;

text = document.getElementById("inner");
text.innerText = words[i];
text.style.color = colors[i];
text.style.fontWeight = "thin";

i += 1;

setInterval(function () {
    changeText();
}, 500);

function changeText() {
    if (i === words.length) {
        i = 0;
    }


    // Change stuff
    text.innerText = words[i];
    text.style.color = colors[i];


    i += 1;
}