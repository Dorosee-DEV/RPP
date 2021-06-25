// downloadCSV = () => {
    
//     var content = 'test';
//     var downloadLink = document.createElement("a");
//     var blob = new Blob(["\ufeff"+content], { "type" : "text/csv;charset=utf-8"});

//     downloadLink.href = window.URL.createObjectURL(blob);
//     downloadLink.download = "Result.csv";
//     downloadLink.click();

// }




// sample csv파일 다운로드
function down_csv(){
    //window.location.assign('csv_sample.zip');
    window.location.assign('../static/GUI/sample/csv_sample.zip');
}


// manual 다운로드
function down_inf(){
    window.location.assign('GUI/sample/manual_sample.hwp');
}

// result csv 다운로드
function down_rst(){
    window.location.assign('GUI/sample/result.csv');
}



// function downloadFile(){
//    const blob = new Blob(["\ufeff"+this.content], {type: "text/csv;charset=utf-8"})
//    const url = window.URL.createObjectURL(blob)
//    const a = document.createElement("a")
//    a.href = "../HPMS.csv"
//    a.download = `${this.$store.state.nickname}_${this.title}.md`
//    a.click()
//    a.remove()
//    window.URL.revokeObjectURL(url);
// }



function reset(){
    var input = document.createElement("input");
    input.type = "submit";
    input.onclick = resetText();
    if ($('table').is(':visible')) {
        $('table').hide()
      }
}



function resetText(){

    var pText1 = document.getElementById("p1");
    var pText2 = document.getElementById("p2");
    var pText3 = document.getElementById("p3");
    var pText4 = document.getElementById("p4");
    var pText5 = document.getElementById("p5");

    pText1.innerText = "";
    pText2.innerText = "";
    pText3.innerText = "";
    pText4.innerText = "";
    pText5.innerText = "";
    document.getElementById("year").value='';
    document.getElementById("km").value='';

}

var input = document.createElement("input");
var input2 = document.createElement("input");
var input3 = document.createElement("input");
var input4 = document.createElement("input");
var input5 = document.createElement("input");



function selectCsv1(){
    const form2 = document.getElementById('form2');
    var ipsubmit = document.createElement("input");
    input.id = "input1";
    input.name = "input1";
    input.type = "file";
    input.style = "display:none";
    input.click();

    ipsubmit.type ="submit";
    ipsubmit.value = "년도확인";

    input.addEventListener('change', update1);
    console.log(form2);
    form2.appendChild(input);
    form2.appendChild(ipsubmit);
    }

function update1(event){

console.log(event.target.files[0].name);

var fileName = event.target.files[0].name;
var fileType = fileName.slice(fileName.indexOf(".") + 1).toLowerCase();
console.log(fileName);
console.log(fileType);
var sc1 = document.getElementById("sc1");


var pText = document.getElementById("p1");
    if(fileType == "csv"){
        pText.innerText = fileName + "uploaded successfully"
        pText.style.color = "#08D403";
        }
    else {
        pText.innerText = "wrong data";
        pText.style.color = "#FF0000";
    }

}



function selectCsv2(){
    const form = document.getElementById('form1');
    input2.id = "input2"
    input2.name = "input2"
    input2.type = "file";
    input2.style = "display:none";
    input2.click();

    input2.addEventListener('change', update2);
    form.appendChild(input2);
    }

function update2(event){

console.log(event.target.files[0].name);

var fileName = event.target.files[0].name;
var fileType = fileName.slice(fileName.indexOf(".") + 1).toLowerCase();

console.log(fileType);

var pText = document.getElementById("p2");

    if(fileType == "csv"){
        pText.innerText = fileName + "uploaded successfully"
        pText.style.color = "#08D403";
        }
    else {
        pText.innerText = "wrong data";
        pText.style.color = "#FF0000";
    }

}



function selectCsv3(){
    const form = document.getElementById('form1');
    input3.id = "input3"
    input3.name = "input3"
    input3.type = "file"
    input3.style = "display:none";
    input3.click();

    input3.addEventListener('change', update3);
    form.appendChild(input3);
    }

function update3(event){

console.log(event.target.files[0].name);

var fileName = event.target.files[0].name;
var fileType = fileName.slice(fileName.indexOf(".") + 1).toLowerCase();

console.log(fileType);

var pText = document.getElementById("p3");

    if(fileType == "csv"){
        pText.innerText = fileName + "uploaded successfully"
        pText.style.color = "#08D403";
        }
    else {
        pText.innerText = "wrong data";
        pText.style.color = "#FF0000";
    }

}



function selectCsv4(){
    const form = document.getElementById('form1');
    input4.id = "input4"
    input4.name = "input4"
    input4.type = "file"
    input4.style = "display:none";
    input4.click();

    input4.addEventListener('change', update4);
    form.appendChild(input4);
    }

function update4(event){

console.log(event.target.files[0].name);

var fileName = event.target.files[0].name;
var fileType = fileName.slice(fileName.indexOf(".") + 1).toLowerCase();

console.log(fileType);

var pText = document.getElementById("p4");

    if(fileType == "csv"){
        pText.innerText = fileName + "uploaded successfully"
        pText.style.color = "#08D403";
        }
    else {
        pText.innerText = "wrong data";
        pText.style.color = "#FF0000";
    }

}



function selectCsv5(){
    const form = document.getElementById('form1');
    input5.id = "input5"
    input5.name = "input5"
    input5.type = "file"
    input5.style = "display:none";
    input5.click();

    input5.addEventListener('change', update5);
    form.appendChild(input5);
    }

function update5(event){

console.log(event.target.files[0].name);

var fileName = event.target.files[0].name;
var fileType = fileName.slice(fileName.indexOf(".") + 1).toLowerCase();

console.log(fileType);

var pText = document.getElementById("p5");

    if(fileType == "csv"){
        pText.innerText = fileName + "uploaded successfully"
        pText.style.color = "#08D403";
        }
    else {
        pText.innerText = "wrong data";
        pText.style.color = "#FF0000";
    }

}

function showTable() {
     console.log("showTable CALLED")
     table = document.getElementById("rst01")
     table.style.visibility = "visible"
   // location.href = 'localhost:5000/execute2';
}