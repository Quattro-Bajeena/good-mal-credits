
let bar = document.getElementById("pageDownloadBar");
console.log(bar)

function change_bar_fill(current, max){

    console.log(current, max);
    let percent = parseInt(current) / parseInt(max);
    

    if(typeof(percent) == 'number'){
        var new_width =  (percent * 100) + '%';
    }
    else{
        var new_width = '100%'
    }


    console.log(percent, new_width);
    bar.style.width = new_width;
}

//progress_url

let interval_id = setInterval(update_bar, 2000)
function update_bar(){
    fetch(progress_url)
    .then(response => response.json())
    .then(response => {
        console.log(response);

        change_bar_fill(response['info']['current'],response['info']['total'] );
        if(response['state'] == 'SUCCESS') {
            clearInterval(interval_id);
            console.log("interval cleared");
        }
    })
}


