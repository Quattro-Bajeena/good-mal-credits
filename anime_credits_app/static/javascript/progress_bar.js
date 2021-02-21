const barFill = document.getElementById("pageDownloadBar");
const barStatus = document.getElementById("pageDownloadStatus");

function change_bar_fill(current, max, transition_duration){

    //console.log(current, max);
    barFill.style.transitionDuration = transition_duration;

    let new_width;
    if (typeof current == 'number' && typeof max == 'number'){
        let percent = current / max;
        //console.log(percent);
        new_width =  (percent * 100) + '%';
    }
    else{
        new_width = '0%';
    }

    //console.log(new_width);
    barFill.style.width = new_width;
}

function change_bar_description(description){

    let text;
    //console.log(description);
    if(typeof description == 'string'){
        text = description;
    }
    else{
        text = "starting";
    }
    barStatus.innerText = text;
    
}


let interval_time = 1000;
let pending;
function update_bar(){
    
    fetch(progress_url)
    .then(response => response.json())
    .then(response => {
        //console.log(response);
        
        //is this the cause of this weird hiccup at the beggin? is it still nececarry?
        // if(pending == true && response['info'] != null){
        //     //State pending
        //     pending = false;
        //     window.location.reload();
        // }

        if(response['state'] == 'SUCCESS') {
            change_bar_description("Download completed");
            change_bar_fill(1,1, interval_time);

            setTimeout( () => {
                window.location.reload();
            }, 1000)
        }
        else if(response['state'] == 'FAILURE'){
            change_bar_description("Download failure");
            barFill.style['background-color'] = 'gray';
        }
        else if(response['info'] != null){
            //normal download situation
            
            change_bar_description(response['info']['status']);
            change_bar_fill(response['info']['current'],response['info']['total'], interval_time );
            setTimeout(update_bar, interval_time);
        }
        else if(response['state'] == 'PENDING') {
            pending = true;
            setTimeout(update_bar, 10000);
        }
        else{

            setTimeout(update_bar, interval_time * 4);
        }
    })
    .catch(error => {
        change_bar_description("Error: Couldn't retrieve progress data");
        
        console.log("Error: Couldn't retrieve progress data");
        console.log(response);
        console.log(error);
    });


}


update_bar()



