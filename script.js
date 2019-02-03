var imageFile;

function detectFromUrl() {
	var imageUrl = document.getElementById('image-url').value;
	$.ajax({
		type: "GET",
		url: "http://localhost:5000/api/detect/from-url",
		contentType: "application/json; charset=utf-8",
		data: {"url": imageUrl},
		success: function(data) {
            $("#result").css("display","block");
            $("#result ul").html("<li>Faces detectadas: " + data.faces_detected + "</li>");
			if(data.faces_detected > 0) {
			    $("#card-orig").css("display", "inline-block");
			    $("#card-result").css("display", "inline-block");

			    $("#image-orig").attr("src", imageUrl);
			    $("#image-result").attr("src", data.result_image.base64_image);
                
                $("#result ul").append("<li>Resolução da imagem: " + data.result_image.resolution + " px</li>");
                $("#result ul").append("<li>Informações das faces:</li><ul id='face_list'></ul>");
                data.face_list.forEach(function(current) {
                    $("#face_list").append("<ul style='margin-bottom: 10px'><li>id: " + current.id + "</li><li>x: " + current.x + "px</li><li>y: " + current.y + "px</li><li>largura: " + current.width + "</li><li>altura: " + current.height + "</li></ul>");
                });
            } else {
                $("#card-orig").css("display", "inline-block");
			    $("#card-result").css("display", "none");

			    $("#image-orig").attr("src", imageUrl);
            }
		},
        error: function (error) {
            console.log(error);
            alert(error.responseText);
        }
	});
}

function detectFromFile() {
	$.ajax({
		type: "GET",
		url: "http://localhost:5000/api/detect/from-file",
		contentType: "application/json; charset=utf-8",
		data: {"file": imageFile},
		success: function(data) {
            $("#result").css("display","block");
            $("#result ul").html("<li>Faces detectadas: " + data.faces_detected + "</li>");
            if(data.faces_detected > 0) {
			    $("#card-orig").css("display", "inline-block");
			    $("#card-result").css("display", "inline-block");

			    $("#image-orig").attr("src", imageFile);
			    $("#image-result").attr("src", data.result_image.base64_image);
        
                $("#result ul").append("<li>Resolução da imagem: " + data.result_image.resolution + " px</li>");
                $("#result ul").append("<li>Informações das faces:</li><ul id='face_list'></ul>");
                data.face_list.forEach(function(current) {
                    $("#face_list").append("<ul style='margin-bottom: 10px'><li>id: " + current.id + "</li><li>x: " + current.x + "px</li><li>y: " + current.y + "px</li><li>largura: " + current.width + "</li><li>altura: " + current.height + "</li></ul>");
                });
            } else {
                $("#card-orig").css("display", "block");
			    $("#card-result").css("display", "none");

			    $("#image-orig").attr("src", imageFile);
            }
		},
        error: function(error) {
            console.log(error);
            alert(error.responseText);
        }
	});
}

function readURL(input) {
	if(input.files && input.files[0]) {
		var reader = new FileReader();
		reader.onload = function(e) {
			imageFile = e.target.result;
		};
		reader.readAsDataURL(input.files[0]);
	}
}

function init() {
	var input = document.getElementById("image-url");
	input.addEventListener("keyup", function(event) {
		event.preventDefault();
		if (event.keyCode === 13) {
			document.getElementById("btn-url").click();
		}
	});
	input = document.getElementById("image-file");
	input.addEventListener("keyup", function(event) {
		event.preventDefault();
		if (event.keyCode === 13) {
			document.getElementById("btn-file").click();
		}
	});
}
