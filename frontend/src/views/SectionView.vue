<script setup>
import FeedMethodsAPI from '../api/resources/FeedMethods.js';
import Problem from '../components/Problem.vue';
import { ref } from 'vue';

const props = defineProps(['id'])

const data = ref({})
data.value = await FeedMethodsAPI.index_section(props.id);
const items = data.value.data;
</script>

<template>
    <h2>Problems on section {{ props.id }}</h2>

    <p>Hold colors used: <span class="label" :class="color" v-for="(c, color) in data.colors">{{ c }}</span></p>

    <div class="flex two">
        <div v-for="item in items" :key="item.id">
            <Problem :data="item" slim="yes"></Problem>
        </div>
    </div>
</template>

<style scoped>
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
