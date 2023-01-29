<script setup>
import FeedMethodsAPI from '../api/resources/FeedMethods.js';
import Problem from '../components/Problem.vue';
import { ref } from 'vue';

const props = defineProps(['id'])

const items = ref([]);
const colors = ref({});
const grades = ref({})

async function refresh() {
    const data = await FeedMethodsAPI.index_section(props.id);
    items.value = data.data;
    colors.value = data.colors;
    grades.value = data.grades
}
await refresh();
// refresh on visibilitychange (switching to the app)
window.addEventListener('visibilitychange', async () => {
    if (document.visibilityState === 'visible') {
        await refresh();
    }
});
</script>

<template>
    <h2>Problems on section {{ props.id }}</h2>

    <div class="flex two">
        <div>Hold colors used</div>
        <div class="right"><span class="label" :class="color" v-for="(c, color) in colors">{{ c }}</span></div>
        <div>Grades</div>
        <div class="right"><span class="label" :class="color" v-for="(c, color) in grades">{{ c }}</span></div>
    </div>

    <div class="flex two">
        <div v-for="item in items" :key="item.id">
            <Problem :data="item" slim="yes"></Problem>
        </div>
    </div>
</template>

<style scoped>
div.right {
    text-align: right;
}

h2 {
    padding: 0;
}

td.name {
    width: 72%;
}

td {
    padding-right: 0.1em;
    padding-left: 0;
}

tr td:first-child {
    padding-left: 0.3em;
}

tr td:last-child {
    padding-right: 0.3em;
}

span.grade {
    width: 5em;
}

td.section {
    text-align: center;
}

span.label {
    margin-left: 0;
}
</style>
