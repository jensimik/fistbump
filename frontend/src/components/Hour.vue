<script setup>
import HourMethodsAPI from '../api/resources/HourMethods.js';
import { ref } from 'vue';

const hours = ref({});
hours.value = await HourMethodsAPI.index();
</script>

<template>
    <h2>Hours <span class="small">(<a href="https://kulturogfritidn.kk.dk/noerrebrohallen">nørrebrohallen</a>)</span>
    </h2>
    <div>{{ hours.hours_today }}</div>
</template>