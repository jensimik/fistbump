<script setup>
import CalendarMethodsAPI from '../api/resources/CalendarMethods.js';
import { ref } from 'vue';

const items = ref([]);
items.value = await CalendarMethodsAPI.index();
</script>

<template>
    <table class="primary">
        <thead>
            <tr>
                <th colspan="2">Calendar</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in items" v-if="items.length">
                <td>{{ item.hour }}</td>
                <td>{{ item.title }}</td>
            </tr>
            <tr v-else>
                <td colspan="2">empty calendar for today</td>
            </tr>
        </tbody>
    </table>
</template>