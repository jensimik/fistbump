<script setup>
import CalendarMethodsAPI from '../api/resources/CalendarMethods.js';
import { ref } from 'vue';

const items = ref([]);
items.value = await CalendarMethodsAPI.index();
</script>

<template>
    <h2>Calendar <span class="small">(<a href="https://nkk.klub-modul.dk/cms/Activity.aspx">klubmodul</a>)</span></h2>
    <table class="primary" v-if="items.length">
        <tbody>
            <tr v-for="item in items">
                <td>{{ item.time }}</td>
                <td>{{ item.title }}</td>
            </tr>
        </tbody>
    </table>
    <div v-else>
        empty calendar for today
    </div>
</template>