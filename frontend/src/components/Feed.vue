<script setup>
import FeedMethodsAPI from '../api/resources/FeedMethods.js';
import { ref } from 'vue';

const items = ref([]);
items.value = await FeedMethodsAPI.index();
</script>

<template>
    <h2>Problems</h2>
    <table class="primary">
        <tbody>
            <tr v-for="item in items">
                <td>-{{ item.days_back }}d</td>
                <td>{{ item.section }}: {{ item.name }} {{ item.grade }}</td>
            </tr>
        </tbody>
    </table>
</template>