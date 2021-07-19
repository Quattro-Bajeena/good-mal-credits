'use strict';

const numberDisplay = document.getElementById("numberDisplay");
const thresholdSlider = document.getElementById("thresholdSlider");


function updateNumberDisplay(event) {
    numberDisplay.value=event.target.value; 
}

thresholdSlider.addEventListener("input", updateNumberDisplay);

const url = new URL(window.location.href);
const threshold = url.searchParams.get("threshold");

if(threshold){
    thresholdSlider.value = threshold;
    numberDisplay.value = threshold;
}
else{
    thresholdSlider.value = 0;
    numberDisplay.value = 0;
}
