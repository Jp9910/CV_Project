// const fs = require('fs');
// const path = require('path');
// require() só funciona server-side (node.js). Esse javascript ta sendo executado no cliente (ou seja, não tem acesso ao filesystem)
// https://www.w3schools.com/js/js_modules.asp
// O fine-tuning com os dados da base de dados já coletada só funcionaria num ambiente nodejs

// Notice there is no 'import' statement. 'mobilenet' and 'tf' is
// available on the index-page because of the script tag above.
let modelo;

const STATUS = document.getElementById('status');
STATUS.innerText = 'Loaded TensorFlow.js - version: ' + tf.version.tfjs;

const PREDICT_BUTTON = document.getElementById('bt-predict');
const CANVAS = document.getElementById("canvas")
const RESULT = document.getElementById("resultado")
const MOBILE_NET_INPUT_WIDTH = 512;
const MOBILE_NET_INPUT_HEIGHT = 512;
const CLASS_NAMES = ["aurelion sol", "kindred", "teemo"];
const ctx = CANVAS.getContext("2d");
const MSG_RESULTADO = document.getElementById("msg-resultado")

PREDICT_BUTTON.addEventListener('click', predict);

const loaderContainer = document.querySelector('.loader-container');

// Chamar função async pra considerar o gif de loading
// (async() => {
// 	loaderContainer.style.display = 'block';
// 	await loadModel();
// 	loaderContainer.style.display = 'none';
// })();

loadModel();
setupCanvas();
setupCanvasNavbar();

async function predict() {
	let imageAsTensor = tf.browser.fromPixels(CANVAS); // Parameters:
													// 1 - pixels (ImageData|HTMLImageElement|HTMLCanvasElement|HTMLVideoElement) 
													//	The input image to construct the tensor from. The supported image types are all 4-channel.
													// 2 - numChannels (number) The number of channels of the output tensor. A numChannels 
												 	//	value less than 4 allows you to ignore channels. Defaults to 3 (ignores alpha channel of input image)

	let resized = tf.image.resizeBilinear(imageAsTensor, [MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH], true);
	let normalized = resized.div(255); // dividir por 255
	const resultado = modelo.predict(normalized.expandDims()); // O resultado é um tensor do tensorflow

	let prediction = resultado.squeeze(); //Removes dimensions of size 1 from the shape of a tensor.

	let highestIndex = prediction.argMax().arraySync(); // arraySync transforma o tensor em um array javascript
	console.log("highestindex: ", highestIndex)

	let probabilidades = tf.softmax(prediction) // tensor do tensorflow
	probabilidades = probabilidades.arraySync() // array javascript
	console.log("Probabilidades: ", probabilidades)

	RESULT.scrollIntoView({behavior: 'smooth'});
	MSG_RESULTADO.innerText = "I think you drew:"
	RESULT.innerText = CLASS_NAMES[highestIndex] + ' (Confidence of ' + (probabilidades[highestIndex]*100).toFixed(1) + '%)';
}

/**
 * Loads the MobileNet model and warms it up so ready for use.
 **/
async function loadModel() {
	const URL = 
		'https://raw.githubusercontent.com/Jp9910/Projeto-AM/main/models/tensorflowjs/';

	//https://js.tensorflow.org/api/latest/#loadGraphModel
	modelo = await tf.loadGraphModel(URL, {fromTFHub: true});
	STATUS.innerText = 'Model loaded succesfully!';

	// Warm up the model by passing zeros through it once.
	tf.tidy(function () {
	  let answer = modelo.predict(tf.zeros([1, MOBILE_NET_INPUT_HEIGHT, MOBILE_NET_INPUT_WIDTH, 3]));
	  console.log(answer);
	});
}

function setupCanvas() {
	CANVAS.height = window.innerHeight;
	CANVAS.width = window.innerWidth;
	// ctx is the context of our canvas
	// we use ctx to draw on the canvas

	let draw = false
	let prevX = null
	let prevY = null
	ctx.lineWidth = 4

	// Set draw to true when mouse is pressed
	CANVAS.addEventListener("mousedown", (e) => draw = true)
	// Set draw to false when mouse is released
	window.addEventListener("mouseup", (e) => draw = false)

	CANVAS.addEventListener("mousemove", (e) => {
		// initially previous mouse positions are null
		// so we can't draw a line
		if(prevX == null || prevY == null  || !draw) {
			// Set the previous mouse positions to the current mouse positions
			prevX = e.clientX
			prevY = e.clientY
			return
		}

		// Current mouse position
		let currentX = e.clientX
		let currentY = e.clientY
		console.log(currentX,currentY)

		// Drawing a line from the previous mouse position to the current mouse position
		ctx.beginPath()
		ctx.moveTo(prevX, prevY)
		ctx.lineTo(currentX, currentY)
		ctx.stroke()

		// Update previous mouse position
		prevX = currentX
		prevY = currentY
	})
}

function setupCanvasNavbar() {
	// Selecting all the div that has a class of clr
	let clrs = document.querySelectorAll(".clr")

	// Converting NodeList to Array
	clrs = Array.from(clrs)

	clrs.forEach(clr => {
		clr.addEventListener("click", () => {
			ctx.strokeStyle = clr.dataset.clr
		})
	})

	let clearBtn = document.querySelector(".clear")
	clearBtn.addEventListener("click", () => {
		// Clearning the entire canvas
		ctx.clearRect(0, 0, CANVAS.width, CANVAS.height)
	})

	// Saving drawing as image
	let saveBtn = document.querySelector(".save")
	saveBtn.addEventListener("click", () => {
		let data = CANVAS.toDataURL("image/png", 1)
		let link = document.querySelector("#download-link")
		link.download = "sketch.png"
		link.href = data
		link.click()

		// link.href = data.replace("image/png", "image/octet-stream"); //octet-stream?
		// link.click();
	})
}