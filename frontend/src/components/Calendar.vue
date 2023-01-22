<script setup>
import CalendarMethodsAPI from '../api/resources/CalendarMethods.js';
import { ref } from 'vue';

const items = ref([]);
items.value = await CalendarMethodsAPI.index();
</script>

<template>
    <h2>Calendar</h2>
    <table class="primary" v-if="items.length">
        <tbody>
            <tr v-for="item in items">
                <td>{{ item.hour }}</td>
                <td>{{ item.title }}</td>
            </tr>
        </tbody>
    </table>
    <div v-else>
        empty calendar for today
    </div>
</template>