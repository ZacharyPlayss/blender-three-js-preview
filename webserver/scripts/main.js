import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import GUI from 'lil-gui';
import { createPositionSliders, createRotationSliders, createScaleSliders, createAllTransformSliders,saveGuiState } from 'lil-gui-helper';

const gui = new GUI();

// FUNCTIONS
function handleWindowResize() {
    const { clientWidth, clientHeight } = canvas;
    camera.aspect = clientWidth / clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(clientWidth, clientHeight);
}

function configureDracoLoader(gltfLoader) {
    if (!(gltfLoader instanceof GLTFLoader)) {
        throw new Error('The first parameter must be an instance of THREE.GLTFLoader');
    }
    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('https://cdn.jsdelivr.net/npm/three@0.172.0/examples/jsm/libs/draco/');
    gltfLoader.setDRACOLoader(dracoLoader);
}

function loadModel(url) {
    let name = url.substring(url.lastIndexOf('/') + 1);
    name = name.substring(0, name.lastIndexOf('.'));
    console.log(name);
    return new Promise((resolve, reject) => {
        loader.load(
            url,
            (gltf) => {
                gltf.scene.name = name;
                resolve(gltf.scene);
            },
            (xhr) => {
                console.log(Math.round(xhr.loaded / xhr.total * 100) + '% loaded');
            },
            (error) => {
                console.error('Error loading model:', error);
                reject(error);
            }
        );
    });
}

// SCENE SETUP
const canvas = document.querySelector('#threejs-canvas');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff); // Set background to white

// CAMERA
const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
camera.position.set(5, 5, 5);

// RENDERER
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(canvas.clientWidth, canvas.clientHeight);

const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
keyLight.position.set(5, 10, 5);
keyLight.castShadow = true;
scene.add(keyLight);

const fillLight = new THREE.DirectionalLight(0xffffff, 0.7);
fillLight.position.set(-5, 5, 5);
scene.add(fillLight);

const backLight = new THREE.DirectionalLight(0xffffff, 0.8);
backLight.position.set(0, 5, -10);
scene.add(backLight);

// Ambient light for subtle base lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.3);
scene.add(ambientLight);

// FLOOR PLANE
const floorGeometry = new THREE.PlaneGeometry(50, 50);
const floorMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff, side: THREE.DoubleSide });
const floor = new THREE.Mesh(floorGeometry, floorMaterial);
floor.rotation.x = -Math.PI / 2;
floor.position.y = -1;
floor.receiveShadow = true;
//scene.add(floor);

//GROUND GRID PLANE
const gridHelper = new THREE.GridHelper(20,20);
scene.add(gridHelper);

const guiGridFolder = gui.addFolder("Ground grid")
guiGridFolder.add(gridHelper, 'visible').onChange(() => saveGuiState(gui));


// DRACO LOADER CONFIG
const loader = new GLTFLoader();
configureDracoLoader(loader);

// LOAD CUSTOM MODEL
let monkey1 = await loadModel('../assets/models/model.glb');
monkey1.position.y = 0.5; // Place above floor
scene.add(monkey1);
createPositionSliders(gui, monkey1, -5, 5);

//RESET THE GUI VALUES FROM LOCALSTORAGE
const savedGuiState = localStorage.getItem("lilGuiState");

if(savedGuiState !== null){
    gui.load(JSON.parse(savedGuiState))
}

// CONTROLS
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.5, 0); // Look at floor level
controls.update();

// ANIMATE
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
    controls.update();
}
handleWindowResize();
animate();

// GLOBAL EVENT LISTENERS
window.addEventListener('resize', handleWindowResize);
