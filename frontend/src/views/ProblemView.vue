<script setup>
import FeedMethodsAPI from '../api/resources/FeedMethods.js';
import { ref } from 'vue';

const props = defineProps(['id'])

function gradeToColor(grade) {
    switch (grade.toUpperCase()) {
        case "?":
            return "turquoise";
        case "4":
            return "green";
        case "let":
            return "green";
        case "5+":
            return "orange";
        case "5B":
            return "orange";
        case "5B+":
            return "orange";
        case "5B-5B+":
            return "orange";
        case "5C":
            return "blue";
        case "5C+":
            return "blue";
        case "6A":
            return "blue";
        case "6A+":
            return "blue";
        case "6B":
            return "purple";
        case "6B+":
            return "purple";
        case "6C":
            return "red";
        case "6C+":
            return "red";
        case "7A":
            return "brown";
        case "7A+":
            return "brown";
        case "7B":
            return "black";
        case "7B+":
            return "black";
        case "7C":
            return "black";
        case "7C+":
            return "pink";
        case "8A":
            return "pink";
    }
}
const item = ref({});
item.value = await FeedMethodsAPI.get(props.id);
</script>

<template>
    <h2>{{ item.name }} ({{ item.section }}) <span class="label"
            :style="{ backgroundColor: gradeToColor(item.grade) }">{{
                item.grade
            }}</span></h2>

    <div v-if="item.section == 'Ö'">
        <svg width="100%" viewBox="0 0 2330 3000" xmlns="http://www.w3.org/2000/svg">
            <image href="@/assets/stokt-wall.jpg" height="3000" width="2330" />
            <path class="hold" d="M362.67,2299.03L317.09,2302.68L312.84,2336.68L356.51,2342.14z"></path>
        </svg>
        STÖKT
    </div>
    <div v-else>
        BOULDER
    </div>
</template>

<style scoped>
span.label {
    width: 3.5em;
}


.hold {
    stroke: white;
    stroke-width: 10px;
    fill: none;
}
</style>