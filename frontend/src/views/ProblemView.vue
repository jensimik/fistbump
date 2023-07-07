<script setup>
import Layout from '../components/Layout.vue';
import ProblemsMethodsAPI from '../api/resources/ProblemsMethods.js';
import Problem from '../components/Problem.vue'
import { setter_auth } from '../localStorage';

import { ref } from 'vue';

const props = defineProps(['id'])

const item = ref({});
item.value = await ProblemsMethodsAPI.get(props.id);
</script>

<template>
    <Layout>
        <template v-slot:menu>
            <router-link v-if="item.section.startsWith('S') && setter_auth" class="button" :to="{ name: 'problem_edit', params: { id: item.id } }">edit</router-link>
        </template>
        <template v-slot:content>
            <Problem :data="item" :auth="setter_auth"></Problem>
        </template>
    </Layout>
</template>
