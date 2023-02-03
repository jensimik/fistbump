<script setup>
import ProblemsMethodsAPI from '../api/resources/ProblemsMethods.js';
import router from '../router/index.js';
import { ref } from 'vue';
import { name, setter_auth } from '../localStorage';

const data = ref({
  name: "",
  grade: "6A",
  section: "S1",
  color: "",
  setter: name,
  text: "",
  error: "",
  button_disabled: false,
  button_text: "add"
});

const preview = ref(null);
const image = ref(null);
const image_size = ref({ width: 0, height: 0 });
const annotations = ref([]);

const add_circle = async (e) => {
  console.log(e);
  const { farthestViewportElement: svgRoot } = e.target;
  let pt = DOMPoint.fromPoint(svgRoot);
  pt.x = e.clientX;
  pt.y = e.clientY;
  let cpt = pt.matrixTransform(svgRoot.getScreenCTM().inverse())
  annotations.value.push({ cx: cpt.x, cy: cpt.y })
}

const remove_circle = async (id) => {
  annotations.value.splice(id, 1);
}

async function add(e) {
  data.value.button_disabled = true
  data.value.button_text = "working..."
  data.value.error = ""
  let formData = new FormData()
  formData.set('name', data.value.name)
  formData.set('color', data.value.color)
  formData.set('grade', data.value.grade)
  formData.set('section', data.value.section)
  formData.set('setter', data.value.setter)
  formData.set('text', data.value.text)
  formData.set('file', image.value)
  try {
    const answer = await ProblemsMethodsAPI.store(formData, setter_auth.value)
    router.push({ name: 'problem', params: { id: answer.id } })
  } catch (error) {
    data.value.error = "failed to submit - did you fill out all fields and upload image?"
  }
  data.value.button_text = "add"
  data.value.button_disabled = false
}

function onFileChange(event) {
  var input = event.target;
  if (input.files) {
    var reader = new FileReader();
    reader.onload = (e) => {
      let img = new Image();
      img.onload = () => {
        image_size.value.width = img.width;
        image_size.value.height = img.height;
      }
      img.src = e.target.result;

      preview.value = e.target.result;
    }
    image.value = input.files[0];
    reader.readAsDataURL(input.files[0]);
  }
}
</script>

<template>
  <div class="flex one">
    <div>
      <h2>Add problem</h2>
    </div>
    <div>
      Awesome with a new problem 💪 let's add it
    </div>
    <div>
      <label for="name">Name</label>
      <input v-model="data.name" type="text" required name="name"
        placeholder="give it a good name and tag the tape too" />
      <label for="holdcolor">Holds color</label>
      <select v-model="data.color" name="color">
        <option value="yellow">yellow</option>
        <option value="red">red</option>
        <option value="blue">blue</option>
        <option value="green">green</option>
        <option value="black">black</option>
        <option value="white">white</option>
        <option value="purple">purple</option>
        <option value="brown">brown</option>
        <option value="orange">orange</option>
      </select>
      <label for="grade">Grade</label>
      <select v-model="data.grade" name="grade">
        <option value="4-5A">Green range (4-5A)</option>
        <option value="5B">Yellow soft (5B)</option>
        <option value="5B+">Yellow hard (5B+)</option>
        <option value="5B-5B+">Yellow range (5B-5B+)</option>
        <option value="5C">Blue soft (5C)</option>
        <option value="6A">Blue medium (6A)</option>
        <option value="6A+">Blue hard (6A+)</option>
        <option value="5C-6A+">Blue range (5C-6A+)</option>
        <option value="6B">Purple soft (6B)</option>
        <option value="6B+">Purple hard (6B+)</option>
        <option value="6B-6B+">Purple range (6B-6B+)</option>
        <option value="6C">Red soft (6C)</option>
        <option value="6C+">Red hard (6C+)</option>
        <option value="6C-6C+">Red range (6C-6C+)</option>
        <option value="7A">Brown soft (7A)</option>
        <option value="7A+">Brown hard (7A+)</option>
        <option value="7A-7A+">Brown range (7A-7A+)</option>
        <option value="7B">Black soft (7B)</option>
        <option value="7B+">Black medium (7B+)</option>
        <option value="7C">Black hard (7C)</option>
        <option value="7B-7C">Black range (7B-7C)</option>
        <option value="7C+-8C">Mytical white (7C+-8C)</option>
      </select>
      <label for="section">Section</label>
      <select v-model="data.section" name="section">
        <option value="S1">Section1</option>
        <option value="S2">Section2</option>
        <option value="S3">Section3</option>
        <option value="S4">Section4</option>
        <option value="S5">Section5</option>
      </select>
      <label for="setter">Setter</label>
      <input v-model="data.setter" type="text" name="setter"
        placeholder="setter name - or if do not know then write 'unknown'" />
      <label for="text">Notes</label>
      <input v-model="data.text" type="text" name="text" />
      <label>Image</label>
      <div v-if="preview">
        <svg width="100%" :viewBox="'0 0 ' + image_size.width + ' ' + image_size.height"
          xmlns="http://www.w3.org/2000/svg">
          <image id="svgimg" :href="preview" :height="image_size.height" :width="image_size.width"
            @click="add_circle" />
          <g>
            <circle :cx="a.cx" :cy="a.cy" r="50" stroke-width="15" stroke="#FF4136"
              @touchend="() => remove_circle(index)" @click="() => remove_circle(index)" fill="transparent" :key="index"
              v-for="(a, index) in annotations" />
          </g>
        </svg>
      </div>
      <input name="image" title="Drop image or click me" @change="onFileChange" type="file"
        accept="image/*;capture=camera">
      <p v-if="data.error">{{ data.error }}</p>
      <div class="flex one">
        <div>
          <button class="button addbutton" :disabled="data.button_disabled" @click="add">{{ data.button_text }}</button>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
#svgimg {
  cursor: pointer;
}

.imagecontainer {
  position: relative;
}

.dropimage {
  background-color: transparent;
  background-repeat: no-repeat;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10;
}

.imageupload {
  width: 100%;
  background-repeat: no-repeat;
  background-size: 100%;
}

img.preview {
  width: 100%;
}

button {
  width: 100%;
}
</style>