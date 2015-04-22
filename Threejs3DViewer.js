var scene, camera, renderer, keyboard, tablet, texture, noTexture, text2, axes;

var lambertTexture;
var loadingTextPresent = true;

var delay = 0;
var isLoaded = false;

var textureTimer = true;
var textureOn = true;

var axesOn = true;
var axesTimer = true;

var origin = new THREE.Vector3(0, 0, 0);
var mouse = new THREE.Vector2();

init();
animate();

function init() {
	
	// Create the scene and set the scene size.
	scene = new THREE.Scene();
	var WIDTH = 1000, HEIGHT = 600;

	keyboard = new THREEx.KeyboardState();

	// Create a renderer and add it to the DOM.
	renderer = new THREE.WebGLRenderer( {
		antialias : true
	});
	renderer.setSize(WIDTH, HEIGHT);
	document.body.appendChild(renderer.domElement);

	// Create a camera, zoom it out from the model, and add it to the scene.
	camera = new THREE.PerspectiveCamera(60, WIDTH / HEIGHT, 0.1, 20000);
	camera.position.set(10, 10, 10);
	camera.lookAt(new THREE.Vector3(0, 0, 0));
	scene.add(camera);

//	EVENT LISTENER TO DYNAMICALLY CHANGE THE SIZE OF THE
//	VIEWER IF THE WINDOW IS READJUSTED - REMOVED FOR THE TIME BEING
	
//	window.addEventListener('resize', function() {
//		var WIDTH = 1000, HEIGHT = 600;
//		renderer.setSize(WIDTH, HEIGHT);
//		camera.aspect = WIDTH / HEIGHT;
//		camera.updateProjectionMatrix();
//	});

	text2 = document.createElement('div');
	text2.style.position = 'absolute';
	text2.style.width = 100;
	text2.style.height = 100;
	text2.style.color = "white";
	text2.innerHTML = "LOADING\n. . .";
	text2.style.top = 290 + 'px';
	text2.style.left = 455 + 'px';
	document.body.appendChild(text2);
	
//  LOADING THE OBJECT IN FROM THE /js/ FOLDER
	//tablet_20_tiny_withScalar_workingTex.json
	
	var loader = new THREE.JSONLoader();
	loader.load("js/00025.json", function(object,
			materials) {
		//scene.add(object);
		//var faceMaterial = new THREE. MeshFaceMaterial( materials );
		
		//tablet = new THREE.Mesh(geometry, materials[0]);
		texture = new THREE.MeshFaceMaterial(materials);
		lambertTexture = new THREE.MeshLambertMaterial();
		tablet = new THREE.Mesh(object, texture);
		materials.needsUpdate = true;
		tablet.matrixAutoUpdate = false;
		//tablet = new THREE.Mesh(geometry, new THREE.MeshLambertMaterial(materials));
		//scene.add(tablet);
		//tablet.position.x = -10;
	});
	
// the following ensures that the tablet is added only when it is completely loaded
	loader.onLoadComplete = function() {
		scene.add(tablet)
	};
	
	//builds the colored axis
	axes = buildAxes();
	scene.add(axes);

	// Set the background color of the scene.
	renderer.setClearColor(0x333F47, 1);

	// Create a light, set its position, and add it to the scene.
	var light = new THREE.SpotLight(0xffffff, 1);
	light.position.set(-10, 20, 10);
	scene.add(light);

	var light2 = new THREE.SpotLight(0xffffff, 1);
	light2.position.set(100, -200, -100);
	scene.add(light2);

	THREE.DefaultLoadingManager.onProgress = function ( item, loaded, total ) {
	    console.log( item, loaded, total );
	    isLoaded = true;
	};
	
	//Orbit controls
	//consider fixed controls with movable object and fixed camera

	controls = new THREE.TrackballControls(camera, renderer.domElement);
	//it is possible to disable pan and zoom functions
	controls.rotateSpeed = 2.5;
	controls.zoomSpeed = 3;
	controls.panSpeed = 0.8;
	controls.noZoom = false;
	controls.noPan = false;
	controls.staticMoving = true;
	controls.dynamicDampingFactor = 0.3;
}
window.onbeforeunload = function() {
	if(isLoaded){
    scene.remove(tablet);
    tablet.geometry.dispose();
	}
};

function delayUpdate() {
	  if ((new Date().getTime() - delay) > 200){
	      textureTimer = true;
	      axesTimer = true;
	    }
	  }

function animate() {
	requestAnimationFrame(animate);
	if(loadingTextPresent && isLoaded) {loadingTextPresent = false; document.body.removeChild(text2);}
	
	if(isLoaded){
	
	if(!textureTimer || !axesTimer){delayUpdate();}
	
	if(keyboard.pressed("space") && textureTimer)
	{
		textureTimer = false;
		delay = new Date().getTime();
		
		if(textureOn){
			textureOn = false;
			tablet.material = lambertTexture;
		}
		else{
			textureOn = true;
			tablet.material = texture;
		}
	}
	
	if(keyboard.pressed("a") && axesTimer)
	{ 
		axesTimer = false;  
		delay = new Date().getTime(); 
		
		if(axesOn){
			axesOn = false;
			scene.remove(axes);
		}
		else{
			axesOn = true;
			scene.add(axes);
		}
	}	
	controls.update();
	renderer.render(scene, camera);
	}
	
}


//the following code was take from:
//https://github.com/sole/three.js-tutorials/blob/master/object_picking/main.js
//for a simple three dimensional plane indicators
function buildAxes() {
	var axes = new THREE.Object3D();
	axes.add(buildAxis(new THREE.Vector3(0, 0, 0),
			new THREE.Vector3(100, 0, 0), 0xFF0000, false)); // +X
	axes.add(buildAxis(new THREE.Vector3(0, 0, 0),
			new THREE.Vector3(-100, 0, 0), 0x800000, true)); // -X
	axes.add(buildAxis(new THREE.Vector3(0, 0, 0),
			new THREE.Vector3(0, 100, 0), 0x00FF00, false)); // +Y
	axes.add(buildAxis(new THREE.Vector3(0, 0, 0),
			new THREE.Vector3(0, -100, 0), 0x008000, true)); // -Y
	axes.add(buildAxis(new THREE.Vector3(0, 0, 0),
			new THREE.Vector3(0, 0, 100), 0x0000FF, false)); // +Z
	axes.add(buildAxis(new THREE.Vector3(0, 0, 0),
			new THREE.Vector3(0, 0, -100), 0x000080, true)); // -Z
	return axes;
}

function buildAxis(src, dst, colorHex, dashed) {
	var geom = new THREE.Geometry(), mat;
	if (dashed) {
		mat = new THREE.LineDashedMaterial( {
			linewidth : 1,
			color : colorHex,
			dashSize : 50,
			gapSize : 50
		});
	} else {
		mat = new THREE.LineBasicMaterial( {
			linewidth : 1,
			color : colorHex
		});
	}
	geom.vertices.push(src.clone());
	geom.vertices.push(dst.clone());
	var axis = new THREE.Line(geom, mat);
	return axis;
}
