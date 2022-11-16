let fileLoader = document.getElementById("upload");
let imagePreview = document.getElementById("preview");
let outputText = document.getElementById("outputText");
fileLoader.addEventListener("change", fileSelector);


function uploadFile(fileBuf) {
    let req = new XMLHttpRequest();
    req.open("POST", "http://localhost:5000/image");

    req.onreadystatechange = () => {
        if (req.readyState === XMLHttpRequest.DONE && req.status === 200) {
            if (req.responseText != "Incorrect format") {
                outputText.innerHTML = "I think this is <b>" + req.responseText + "</b>";
            }
            else {
                outputText.innerHTML = "Oops! We don't support this image format at the moment";
            }
        }
      }

    req.send(fileBuf);
}


function fileSelector() {
    let fileDetails = fileLoader.files[0];
    let reader = new FileReader();

    previewDisplayed = false;

    reader.addEventListener("load", (event) => {
        if (previewDisplayed === false) {
            imagePreview.src = reader.result;
            previewDisplayed = true;
            reader.readAsArrayBuffer(fileDetails);
        }
        else {
            uploadFile(reader.result);
        }
        
    });

    if (fileDetails) {
        reader.readAsDataURL(fileDetails);
    }
}


