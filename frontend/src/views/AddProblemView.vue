<script setup>
import FeedMethodsAPI from '../api/resources/FeedMethods.js';
import router from '../router/index.js';
import { ref } from 'vue';

const data = ref({
  name: "",
  grade: "6A",
  section: "S1",
  setter: "",
  text: "",
});

const preview = ref(null);
const image = ref(null);

async function add(e) {
  let formData = new FormData()
  formData.set('name', data.value.name);
  formData.set('grade', data.value.grade);
  formData.set('section', data.value.section);
  formData.set('setter', data.value.setter);
  formData.set('text', data.value.text);
  formData.set('file', image.value);
  await FeedMethodsAPI.store(formData)
  router.push({ name: 'home' })
}

function onFileChange(event) {
  var input = event.target;
  if (input.files) {
    var reader = new FileReader();
    reader.onload = (e) => {
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
      <div class="flex one">
        <div class="imagecontainer">
          <img class="preview" :src="preview ? preview : 'https://via.placeholder.com/900x1200'" />
          <label for="image" class="dropimage" :style="{
            backgroundSize: preview ? '50%' : '100%'
          }">
            <input name="image" title="Drop image or click me" @change="onFileChange" type="file"
              accept="image/*;capture=camera">
          </label>
        </div>
      </div>
      <div class="flex one">
        <div>
          <button class="button addbutton" @click="add">add</button>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
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