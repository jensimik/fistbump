<script setup>
import CalendarMethodsAPI from '../api/resources/CalendarMethods.js';
import HourMethodsAPI from '../api/resources/HourMethods.js';
import { ref } from 'vue';

const items = ref([]);
items.value = await CalendarMethodsAPI.index();
const hours = ref({});
hours.value = await HourMethodsAPI.index();

</script>

<template>
    <h2>Calendar <span class="small">(<a href="https://nkk.klub-modul.dk/cms/Activity.aspx">klubmodul</a> | <a
                href="https://kulturogfritidn.kk.dk/noerrebrohallen">nørrebrohallen</a>)</span></h2>

    <div class="flex two">
        <div>{{ hours.hours_today }}</div>
        <div>Opening hours today (2023-01-24)</div>
    </div>

    <div class="flex two" v-for="item in items" v-if="items.length">
        <div>{{ item.time }}</div>
        <div>{{ item.title }}</div>
    </div>
    <div v-else>
        empty klubmodul calendar for today
    </div>
</template>