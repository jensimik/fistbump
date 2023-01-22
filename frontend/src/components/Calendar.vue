<script setup>
import CalendarMethodsAPI from '../api/resources/CalendarMethods.js';
import { ref } from 'vue';

const items = ref([]);
items.value = await CalendarMethodsAPI.index();
</script>

<template>
    <h2>Calendar <span class="small">(<a href="https://nkk.klub-modul.dk/cms/Activity.aspx">klubmodul</a>)</span></h2>

    <div class="flex two" v-for="item in items" v-if="items.length">
        <div class="">{{ item.time }}</div>
        <div class="">{{ item.title }}</div>
    </div>
    <div v-else>
        empty calendar for today
    </div>
</template>