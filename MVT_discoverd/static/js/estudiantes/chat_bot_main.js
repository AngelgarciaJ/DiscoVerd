import * as THREE from "https://cdn.skypack.dev/three@0.129.0/build/three.module.js";
import { OrbitControls } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js";

const container = document.getElementById("container3D");
const containerWidth = 300;
const containerHeight = 300;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, containerWidth / containerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ 
    alpha: true,
    antialias: true 
});
renderer.setSize(containerWidth, containerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

let object, controls;
let mouseX = containerWidth / 2;
let mouseY = containerHeight / 2;

//const objToRender = 'chat-bot';
const modelPath = '/static/js/estudiantes/models/chat-bot/scene.gltf';
const loader = new GLTFLoader();

loader.load(
    modelPath,
    (gltf) => {
        object = gltf.scene;
        
        // Centrar el modelo
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        object.position.x += (object.position.x - center.x);
        object.position.y += (object.position.y - center.y);
        object.position.z += (object.position.z - center.z);
        
        // Ajustar escala si es necesario
        const scale = 1.5; // Ajusta este valor según necesites
        object.scale.set(scale, scale, scale);
        
        scene.add(object);
    },
    (xhr) => {
        console.log((xhr.loaded / xhr.total * 100) + '% loaded');
    },
    (error) => {
        console.error('Error loading model:', error);
    }
);

camera.position.z = 20;

const topLight = new THREE.DirectionalLight(0xffffff, 1);
topLight.position.set(500, 500, 500);
scene.add(topLight);

const ambientLight = new THREE.AmbientLight(0x333333, 5);
scene.add(ambientLight);

controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.screenSpacePanning = false;
controls.minDistance = 10;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI / 2;

// Actualizar mouseX y mouseY relativos al contenedor
container.addEventListener('mousemove', (event) => {
    const rect = container.getBoundingClientRect();
    mouseX = event.clientX - rect.left;
    mouseY = event.clientY - rect.top;
});

function animate() {
    requestAnimationFrame(animate);

    if(object) {
        object.rotation.y += (-3 + mouseX / containerWidth * 3 - object.rotation.y) * 0.05;
        object.rotation.x += (-1.2 + mouseY * 2.5 / containerHeight - object.rotation.x) * 0.05;
    }

    controls.update();
    renderer.render(scene, camera);
}

window.addEventListener('resize', () => {
    // Mantener el aspect ratio y el tamaño del contenedor
    camera.aspect = containerWidth / containerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(containerWidth, containerHeight);
});

animate();