{

const getCellValue = function  (tr, idx) {
    return tr.children[idx].innerText || tr.children[idx].textContent;
} 


// if any of the values arent empty strings or NaNs, then it compares them like numbers, in the other case like strings
const comparer = function(idx, asc){

    function compare_col_idx_function (a, b) {

        function comparison_value( v1, v2) {
            if(v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2)){
                return v1 - v2;
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
    "up" : "⬆",
    "down" : "⬇"
}

arrow = document.createElement("span");
arrow.classList.add("arrow") 

const move_arrow = function(th, asc){
    const direction = asc ? arrows['up'] : arrows['down'];
    arrow.innerText = direction;
    th.appendChild(arrow);
}

const sortTable = function (event){

    const th = event.target;
    const table_body = th.closest('table').querySelector("tbody");
    //console.log(table_body)

    //appendChild moves the node
    
    Array.from(table_body.querySelectorAll('tr:nth-child(n+1)'))
        .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
        .forEach(tr => table_body.appendChild(tr) );
    move_arrow(th, this.asc);
    
}

// do the work...
document.querySelectorAll('.sortableColHeader').forEach(th => th.addEventListener('click', sortTable));


}