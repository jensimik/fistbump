<script setup>
const props = defineProps(['data', 'slim'])

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
    <div v-if="props.slim">
        <p><span class="label holds" :class="item.color">holds</span> <span class="label grade"
                :class="item.grade_class">{{
                    item.grade
                }}</span></p>
        <img :src="item.image" class="problem" />
    </div>
    <div v-else>
        <h2>{{ item.name }} ({{ item.section }}) <span class="label grade" :class="item.grade_class">{{
            item.grade
        }}</span></h2>
        <!-- <router-link :to="{ name: 'problem_edit', params: { id: item.id } }">edit</router-link> -->

        <div v-if="item.section == 'Ö'">
            <p>{{ item.setter }}</p>
            <svg width="100%" viewBox="0 0 2330 3000" xmlns="http://www.w3.org/2000/svg">
                <image href="@/assets/stokt-wall.jpg" height="3000" width="2330" />
                <path class="hold" :class="d.type" :d="d.path" v-for="d in item.paths" />
            </svg>
        </div>
        <div v-else>
            <p>{{ item.setter }} <span class="label holds" :class="item.color">{{ item.color }}</span> holds</p>
            <p v-if="item.text">{{ item.text }}</p>
            <img :src="item.image" class="problem" />
        </div>
    </div>
</template>

<style scoped>
span.grade {
    width: 5em;
}

span.holds {
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

img.problem {
    width: 100%;
}
</style>