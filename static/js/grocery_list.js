const checkboxes = document.querySelectorAll('input[type="checkbox"]')
//step 1: keep track of last checked box
//step 2: is shiftkey down?
    //if yes, check everyhing in btw
      //loop through all boxes again and check all in between
    //if no, just check current box

let lastChecked; //keep track of last checked box

function handleCheck(e){
  let inBetween = false; 
  if (e.shiftKey === true){
    checkboxes.forEach(item => {
       //keep track of in between boxes by toggling inBetween to be true for all boxes in between, and then toggle it back to false after. If you dont understand, go through line by line what happen to each box when click and shift.
       if (item === this || item === lastChecked){
         inBetween = !inBetween;
       }
       //check every box in between
       if (inBetween){
         item.checked = true;
       }
    })
  }
  
  lastChecked = this //keep track of last checked box
}

checkboxes.forEach(item => item.addEventListener('click', handleCheck));