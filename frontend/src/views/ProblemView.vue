<script setup>
import ProblemsMethodsAPI from '../api/resources/ProblemsMethods.js';
import Problem from '../components/Problem.vue'
import { setter_auth } from '../localStorage';

import { ref } from 'vue';

const props = defineProps(['id'])

const item = ref({});
item.value = await ProblemsMethodsAPI.get(props.id);
</script>

<template>
    <Problem :data="item" :auth="setter_auth"></Problem>
</template>
