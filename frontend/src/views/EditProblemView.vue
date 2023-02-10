<script setup>
import ProblemsMethodsAPI from '../api/resources/ProblemsMethods.js';
import router from '../router/index.js';
import { ref } from 'vue';
import { setter_auth } from '../localStorage';

const props = defineProps(['id'])

const data = ref({
    name: "",
    color: "",
    grade: "6A",
    section: "S1",
    setter: "",
    text: "",
    holds_start: 2,
    holds_top: 0,
});

const image_size = ref({ width: 0, height: 0 });
const annotations = ref([]);

const add_circle = async (e) => {
    const { farthestViewportElement: svgRoot } = e.target;
    let pt = DOMPoint.fromPoint(svgRoot);
    pt.x = e.clientX;
    pt.y = e.clientY;
    let cpt = pt.matrixTransform(svgRoot.getScreenCTM().inverse())
    annotations.value.push({ cx: cpt.x, cy: cpt.y })
    e.preventDefault();
}


const remove_circle = async (e, id) => {
    annotations.value.splice(id, 1);
    e.preventDefault();
}

const button_data = ref({
    text: "update",
    disabled: false,
    error: "",
})

const preview = ref(null);
const image = ref(null);

async function update(e) {
    button_data.value.disabled = true
    button_data.value.text = "working..."
    data.value.error = ""
    let formData = new FormData()
    formData.set('name', data.value.name);
    formData.set('color', data.value.color);
    formData.set('grade', data.value.grade);
    formData.set('section', data.value.section);
    formData.set('setter', data.value.setter);
    formData.set('text', data.value.text);
    formData.set('image_height', image_size.value.height);
    formData.set('image_width', image_size.value.width);
    formData.set('annotations', JSON.stringify(annotations.value));
    formData.set('holds_start', data.value.holds_start);
    formData.set('holds_top', data.value.holds_top);
    if (image.value) {
        formData.set('file', image.value);
    }
    try {
        await ProblemsMethodsAPI.update(props.id, formData, setter_auth.value)
        router.push({ name: 'problem', params: { id: props.id } })
    } catch (error) {
        button_data.value.error = "error in data - did you fill out all required fields and attach image?"
    }
    button_data.value.text = "update"
    button_data.value.disabled = false
}
async function remove(e) {
    try {
        await ProblemsMethodsAPI.remove(props.id, setter_auth.value)
        router.push({ name: "home" })
    } catch (error) {
        button_data.value.error = "error in auth"
    }
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
const answer = await ProblemsMethodsAPI.get(props.id);
data.value.name = answer.name;
data.value.setter = answer.setter;
data.value.color = answer.color;
data.value.grade = answer.grade;
data.value.section = answer.section;
data.value.holds_start = answer.holds_start;
data.value.holds_top = answer.holds_top;
data.value.text = answer.text;
annotations.value = answer.annotations;
image_size.value.height = answer.image_height;
image_size.value.width = answer.image_width;
preview.value = `https://fbs.gnerd.dk/static/${answer.image_hex}.jpg`;
</script>

<template>
    <div class="flex one">
        <div>
            <h2>Edit problem {{ data.name }}</h2>
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
                <option value="orange">orange</option>
                <option value="purple">purple</option>
                <option value="brown">brown</option>
                <option value="rainbow">rainbow/mixed</option>
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
                    <image :href="preview" :height="image_size.height" :width="image_size.width" @click="add_circle" />
                    <circle :cx="a.cx" :cy="a.cy" r="80" stroke-width="20" stroke="#fff"
                        @click="(e) => remove_circle(e, index)" fill="transparent" :key="index"
                        v-for="(a, index) in annotations" />
                </svg>
                <label for="holds_start">How many starting holds</label>
                <select v-model="data.holds_start">
                    <option value="0">0</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                </select>
                <label for="holds_top">Finish hold or topout?</label>
                <select v-model="data.holds_top">
                    <option value="0">topout</option>
                    <option value="1">last hold</option>
                    <option value="2">last two holds</option>
                </select>
            </div>
            <input name="image" title="Drop image or click me" @change="onFileChange" type="file"
                accept="image/*;capture=camera">
            <p v-if="button_data.error">{{ button_data.error }}</p>
            <button class="button warning" @click="remove">remove</button>
            <button class="button" :disabled="button_data.disabled" @click="update">{{ button_data.text }}</button>
        </div>
    </div>
</template>


<style scoped>
svg {
    width: 100%;
}

svg>img {
    cursor: pointer;
}

button {
    width: 50%;
}
</style>