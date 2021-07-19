'use strict';
{

const searchBarInput = document.getElementById('searchBarInput');
const invalidSearchSlider = document.getElementById('invalidSearchSlider');
const searchButton = document.getElementById('searchButton');
let button_id = window.localStorage.getItem("picked_category_button_id");


const validInput = function(input){
    return input.trim() != '' && input.trim().length >= 3;
}

const validateSearch = function(){
    return validInput(searchBarInput.value);
}

const savePickedCategory = function(){
    const button = document.querySelector('#searchForm input[type="radio"]:checked');
    window.localStorage.setItem("picked_category_button_id", button.id);
    searchBarInput.setAttribute("placeholder", button.value.toUpperCase());
}

const setPickedCategory = function(){
    button_id = window.localStorage.getItem("picked_category_button_id");

    if(button_id){
        document.getElementById(button_id).checked = true;
        
    }
        
}

const send_search_request = function(event){
    event.preventDefault();
    if(validateSearch()){
        savePickedCategory();
        document.forms['search_form'].submit();
    }
    else{

        invalidSearchSlider.classList.add('slider');
        setTimeout(()=>{
            invalidSearchSlider.classList.remove('slider');
        }, 5000);
    }
}


// Originally inspired by  David Walsh (https://davidwalsh.name/javascript-debounce-function)

// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// `wait` milliseconds.
const debounce = (func, wait) => {
    let timeout;
  
    return function executedFunction(...args) {
      const later = () => {
        timeout = null;
        func(...args);
      };
  
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  };


const searchAutocomplete = document.getElementById('searchAutocomplete');
const autocompleteEntry = searchAutocomplete.querySelector('#autocompleteEntryBase');

const dynamicSearch = function(event){
    const query = searchBarInput.value;
    if(query.trim() != '' && query.trim().length >= 3){

        button_id = window.localStorage.getItem("picked_category_button_id");
        const category = document.getElementById(button_id).value;
        const search_url = `/quick_search/${category}/${query}`;

        //console.log(search_url);
        fetch(search_url)
        .then(response => response.json())
        .then(response => {
            //console.log(response);
            
            while(searchAutocomplete.children.length > 1){
                searchAutocomplete.removeChild(searchAutocomplete.lastChild);
                searchAutocomplete.style['visibility'] = "hidden";
            }

            const results = response['results'];
            for(const result of results){
                
                //Next to do cloneNode apparentyl doesnt exists
                const newEntry = autocompleteEntry.cloneNode(true);
                newEntry.removeAttribute('id');
                newEntry.href = `/${category}/${result['mal_id']}`;
                newEntry.innerText = result['identifier'];
                newEntry.style['display'] = "block";
                searchAutocomplete.appendChild(newEntry);
            }
            if(results.length > 0){
                searchAutocomplete.style['visibility'] = "visible";
            } 
            else{
                searchAutocomplete.style['visibility'] = "hidden";
            }
                
            
            
            
        })
    }
    else{
        while(searchAutocomplete.children.length > 1){
            searchAutocomplete.removeChild(searchAutocomplete.lastChild);
            searchAutocomplete.style['visibility'] = "hidden";
        }
    }
    
}



// Event listenrs
document.querySelectorAll('#searchForm input[type="radio"]').forEach(
    button => button.addEventListener('click', savePickedCategory
    ));
searchButton.addEventListener('click', send_search_request);
searchBarInput.addEventListener('input', debounce(dynamicSearch, 450));



// things that co once page is loaded
savePickedCategory();
setPickedCategory();


}