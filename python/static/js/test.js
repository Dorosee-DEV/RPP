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

    table = document.getElementById("rst01")
    table.style.visibility = "hidden"
}





function selectCsv1(){
    var input = document.createElement("input");
    input.id = "inputTest1"
    input.type = "file";
    input.click();

    input.addEventListener('change', update1);

    }

function update1(event){

console.log(event.target.files[0].name);

var fileName = event.target.files[0].name;
var fileType = fileName.slice(fileName.indexOf(".") + 1).toLowerCase();

console.log(fileType);

var pText = document.getElementById("p1");

    if(fileType == "csv"){
        pText.innerText = "uploaded successfully"
        pText.style.color = "#08D403";
        }
    else {
        pText.innerText = "wrong data";
        pText.style.color = "#FF0000";
    }

}



function selectCsv2(){
    var input = document.createElement("input");
    input.id = "inputTest"
    input.type = "file";
    input.click();

    input.addEventListener('change', update2);

    }

function update2(event){

console.log(event.target.files[0].name);

var fileName = event.target.files[0].name;
var fileType = fileName.slice(fileName.indexOf(".") + 1).toLowerCase();

console.log(fileType);

var pText = document.getElementById("p2");

    if(fileType == "csv"){
        pText.innerText = "uploaded successfully"
        pText.style.color = "#08D403";
        }
    else {
        pText.innerText = "wrong data";
        pText.style.color = "#FF0000";
    }

}



function selectCsv3(){
    var input = document.createElement("input");
    input.id = "inputTest"
    input.type = "file";
    input.click();

    input.addEventListener('change', update3);

    }

function update3(event){

console.log(event.target.files[0].name);

var fileName = event.target.files[0].name;
var fileType = fileName.slice(fileName.indexOf(".") + 1).toLowerCase();

console.log(fileType);

var pText = document.getElementById("p3");

    if(fileType == "csv"){
        pText.innerText = "uploaded successfully"
        pText.style.color = "#08D403";
        }
    else {
        pText.innerText = "wrong data";
        pText.style.color = "#FF0000";
    }

}



function selectCsv4(){
    var input = document.createElement("input");
    input.id = "inputTest"
    input.type = "file";
    input.click();

    input.addEventListener('change', update4);

    }

function update4(event){

console.log(event.target.files[0].name);

var fileName = event.target.files[0].name;
var fileType = fileName.slice(fileName.indexOf(".") + 1).toLowerCase();

console.log(fileType);

var pText = document.getElementById("p4");

    if(fileType == "csv"){
        pText.innerText = "uploaded successfully"
        pText.style.color = "#08D403";
        }
    else {
        pText.innerText = "wrong data";
        pText.style.color = "#FF0000";
    }

}



function selectCsv5(){
    var input = document.createElement("input");
    input.id = "inputTest"
    input.type = "file";
    input.click();

    input.addEventListener('change', update5);

    }

function update5(event){

console.log(event.target.files[0].name);

var fileName = event.target.files[0].name;
var fileType = fileName.slice(fileName.indexOf(".") + 1).toLowerCase();

console.log(fileType);

var pText = document.getElementById("p5");

    if(fileType == "csv"){
        pText.innerText = "uploaded successfully"
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