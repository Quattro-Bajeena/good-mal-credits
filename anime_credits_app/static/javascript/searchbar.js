

valid_input = function(input){
    return input.trim() != '' && input.trim().length >= 3;
}


validate_search = function(){
    return valid_input(document.getElementById('searchBarInput').value);
}

