<script setup>
import StripMethodsAPI from '../api/resources/StripMethods.js';
import { ref } from 'vue';

const strip = ref({});
strip.value = await StripMethodsAPI.index();
</script>

<template>
    <h2>{{ strip.section }} strip {{ strip.date }}</h2>
    <p>{{ strip.setters }} | {{ strip.until }} days left to close the set</p>
    <div><img src="@/assets/nkk-walls.svg" style="width:100%" /></div>
</template>

<style scoped>
h2 {
    padding-bottom:
}

p {
    margin-top: 0;
}
</style>