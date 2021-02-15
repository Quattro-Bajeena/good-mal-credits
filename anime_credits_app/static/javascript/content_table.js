{

const getCellValue = function  (tr, idx) {
    return tr.children[idx].innerText || tr.children[idx].textContent;
} 

const recolorRowBackgrounds = function(visible_rows){
    visible_rows.forEach(tr => tr.style.backgroundColor = "inherit" );
    visible_rows.filter((tr, index) => index%2 == 0).forEach(tr => tr.style.backgroundColor = "rgb(233, 233, 233)");
    //background-color: rgb(233, 233, 233);
}


// SORTING--------------------------------
// if any of the values arent empty strings or NaNs, then it compares them like numbers, in the other case like strings
const comparer = function(idx, asc){

    function compare_col_idx_function (a, b) {

        function comparison_value( v1, v2) {
            v1 = v1.replaceAll(' ', '');
            v2 = v2.replaceAll(' ', '');
            if(v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2)){
                
                return v1- v2;
            }
            else{
                return v1.toString().localeCompare(v2);
            }
        } 
        return comparison_value(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));
    } 

    return compare_col_idx_function;
    
} 

const arrows = {
    "up" : "/static/icons/arrow-up.svg",
    "down" : "/static/icons/arrow-down.svg"
}

const arrow = document.createElement("img");
arrow.classList.add("sortArrow");

const move_arrow = function(th, asc){
    const direction = asc ? arrows['up'] : arrows['down'];
    arrow.src = direction;
    th.appendChild(arrow);
}

const sortTable = function (event){

    const th = event.target.closest('th');
    const table_body = th.closest('table').querySelector("tbody");
    //console.log(table_body)

    //appendChild moves the node
    const visible_rows = Array.from(table_body.querySelectorAll('tr'))
        .filter(tr => {
            return tr.style.display != "none"
        });


    visible_rows
        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
        .forEach(tr => table_body.appendChild(tr) );
    move_arrow(th, this.asc);



    recolorRowBackgrounds(visible_rows);
    
}

// do the work...
document.querySelectorAll('.sortableColHeader').forEach(th => th.addEventListener('click', sortTable));


// HIDE TABLE----------------------------------
const hideTable = function(event){

    const table_body = event.target.closest('table').querySelector('tbody');

    let arrow, display;
    if(table_body.style.display != "none"){
        display = "none";
        arrow = arrows["up"];
    }
    else{
        display = "table-row-group";
        arrow = arrows["down"];
    }

    table_body.style.display = display;
    event.target.src = arrow;
    
}

document.querySelectorAll('.hideTableButton').forEach(button => button.addEventListener('click', hideTable));


//FILTERING------------------------------------------------
const column_filter = function(idx, searched_value){

    function column_filter_idx(tr){
        cell_value = getCellValue(tr, idx);
        return cell_value.toLowerCase().includes(searched_value.toLowerCase());
    }
    return column_filter_idx;
}


const filterTable = function(event){
    
    const th = event.target.closest('th');
    const table_body = th.closest('table').querySelector('tbody');
    const inputs = Array.from(th.closest('table').querySelectorAll('.filterCol input, .filterCol select'));

    const arr = Array.from(table_body.querySelectorAll('tr'));
    let included = arr;

    //console.log(event, th, table_body, inputs, arr);
    for(const input of inputs){
        const value = input.value;
        const this_th = input.closest('th');
        index = Array.from(this_th.parentNode.children).indexOf(this_th);
        included = included.filter(column_filter(index, value));
    }

    const not_included = arr.filter(tr => !included.includes(tr))

    // console.log(searched_values);
    // console.log("included ", included);
    // console.log("not_included ", not_included);

    included.forEach(tr => tr.style.display = "table-row");
    not_included.forEach(tr => tr.style.display = "none");

    recolorRowBackgrounds(included);
}

document.querySelectorAll('.filterCol').forEach(header => header.addEventListener("input" ,filterTable));

const clearFilters = function(event){
    const th = event.target.closest('th');
    const inputs = Array.from(th.closest('table').querySelectorAll('.filterCol input'));

    for(const input of inputs){
        input.value = "";
    }

    const fake_event = {target : th };
    filterTable(fake_event);

}

document.querySelectorAll('.clearFilter').forEach(header => header.addEventListener('click', clearFilters));

// Update filter list with all options available
document.querySelectorAll('.filterList').forEach(
    select => {
        th = select.parentNode;
        const body_rows = Array.from(select.closest('table').querySelector('tbody').querySelectorAll('tr'));
        const index = Array.from(select.closest('tr').children).indexOf(th);
        const values = new Set(body_rows.map(tr => getCellValue(tr, index)));

        for(const value of values){
            const new_option = new Option(value, value);
            select.appendChild(new_option);
        }
        
    })

// Set languge to japanese by deafult
document.querySelectorAll('.languageFilter').forEach(
    select => {
        japanese = Array.from(select.children).filter(option => option.value == "Japanese");
        if(japanese){
            select.value = "Japanese";
        }
        const fake_event = {target : select.closest('th')};
        filterTable(fake_event);
    }
)



}