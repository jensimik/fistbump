<script setup>
import FeedMethodsAPI from '../api/resources/FeedMethods.js';
import Problem from '../components/Problem.vue'
import useLocalStorage from '../useLocalStorage';

import { ref } from 'vue';

const setter_auth = useLocalStorage("setter_auth", "");

const props = defineProps(['id'])

const item = ref({});
item.value = await FeedMethodsAPI.get(props.id);
</script>

<template>
    <Problem :data="item" :auth="setter_auth"></Problem>
</template>
