import * as THREE from "three";
import * as OBC from "openbim-components";
import * as WEBIFC from "web-ifc";

const container = document.getElementById("container");

const components = new OBC.Components();

components.scene = new OBC.SimpleScene(components);
components.renderer = new OBC.PostproductionRenderer(components, container);
components.camera = new OBC.SimpleCamera(components);
components.raycaster = new OBC.SimpleRaycaster(components);

components.init();

components.renderer.postproduction.enabled = true;

const scene = components.scene.get();

components.camera.controls.setLookAt(12, 6, 8, 0, 0, -10);

components.scene.setup();

const grid = new OBC.SimpleGrid(components, new THREE.Color(0x666666));
const customEffects = components.renderer.postproduction.customEffects;
customEffects.excludedMeshes.push(grid.get());

let fragments = new OBC.FragmentManager(components);
let fragmentIfcLoader = new OBC.FragmentIfcLoader(components);

await fragmentIfcLoader.setup();

const excludedCats = [
  WEBIFC.IFCTENDONANCHOR,
  WEBIFC.IFCREINFORCINGBAR,
  WEBIFC.IFCREINFORCINGELEMENT,
];

for (const cat of excludedCats) {
  fragmentIfcLoader.settings.excludedCategories.add(cat);
}

fragmentIfcLoader.settings.webIfc.COORDINATE_TO_ORIGIN = true;
fragmentIfcLoader.settings.webIfc.OPTIMIZE_PROFILES = true;

async function loadIfcAsFragments() {
  const file = await fetch("../viewer/resources/small.ifc");
  const data = await file.arrayBuffer();
  const buffer = new Uint8Array(data);
  const model = await fragmentIfcLoader.load(buffer, "example");
  scene.add(model);
}

loadIfcAsFragments();
