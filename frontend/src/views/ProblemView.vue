<script setup>
import FeedMethodsAPI from '../api/resources/FeedMethods.js';
import Problem from '../components/Problem.vue'
import { ref } from 'vue';

const props = defineProps(['id'])

const item = ref({});
item.value = await FeedMethodsAPI.get(props.id);
</script>

<template>
    <Problem :data="item"></Problem>
</template>
