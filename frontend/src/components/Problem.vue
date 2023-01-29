<script setup>
const props = defineProps(['data', 'slim', 'auth'])

const item = props.data;

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
</script>

<template>
    <div v-if="props.slim" class="slim">
        <div class="imgw">
            <router-link :to="{ name: 'problem', params: { id: item.id } }">
                <img :src="item.image" class="problem" />
            </router-link>
            <span class="label holds big left" :class="item.color">holds</span>
            <span class="label grade big right" :class="item.grade_class">{{
                item.grade
            }}</span>
            <span class="label big setter white">{{ item.name }} ({{ item.setter }})</span>
        </div>
    </div>
    <div v-else>
        <h2>{{ item.name }} ({{ item.section }})</h2>
        <div v-if="item.section == 'Ö'">
            <div class="imgw">
                <svg width="100%" viewBox="0 0 2330 3000" xmlns="http://www.w3.org/2000/svg">
                    <image href="@/assets/stokt-wall.jpg" height="3000" width="2330" />
                    <path class="hold" :class="d.type" :d="d.path" v-for="d in item.paths" />
                </svg>
                <span class="label grade big right" :class="item.grade_class">{{
                    item.grade
                }}</span>
                <span class="label big left white">{{ item.setter }}</span>
            </div>
        </div>
        <div v-else>
            <p v-if="item.text">{{ item.text }}</p>
            <div class="imgw">
                <img :src="item.image" class="problem" />
                <span class="label holds big left" :class="item.color">holds</span>
                <span class="label grade big right" :class="item.grade_class">{{
                    item.grade
                }}</span>
                <span class="label big setter white">{{ item.setter }}</span>
            </div>
            <router-link v-if="props.auth" class="button"
                :to="{ name: 'problem_edit', params: { id: item.id } }">edit</router-link>
        </div>
    </div>
</template>

<style scoped>
.label {
    margin-left: 0;
}

path.hold {
    stroke-width: 15px;
    fill: none;
}

path.foot {
    stroke: #39CCCC;
}

path.hand {
    stroke: #fff;
}

wrapper {
    position: relative;
    display: inline-block;
}

img.problem {
    width: 100%;
    display: block;
}

.imgw {
    position: relative;
}

.big {
    position: absolute;
    border-radius: 0;
    font-size: 1.2em;
    opacity: 0.8;
}

.slim .big {
    font-size: 0.8em;
}

.left {
    top: 0;
    left: 0;
}

.right {
    top: 0;
    right: 0;
}

.setter {
    bottom: 0;
    left: 0;
    font-size: 0.5em !important;
}
</style>