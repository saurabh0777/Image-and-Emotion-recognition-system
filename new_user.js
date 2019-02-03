function ValidateForm() {

    var hasError = false;

    if (document.getElementById('lname').value == "") {
        document.getElementById('wronglname').style.display = "inline";
        hasError = true;
    } else {
        document.getElementById('wrongname').style.display = "none";
    }
        if (document.getElementById('name').value == "") {
        document.getElementById('wrongname').style.display = "inline";
        hasError = true;
    } else {
        document.getElementById('wrongname').style.display = "none";
    }

    return !hasError;
}