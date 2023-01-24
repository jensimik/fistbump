<script setup>
import StripMethodsAPI from '../api/resources/StripMethods.js';
import { ref } from 'vue';

const strip = ref({});
strip.value = await StripMethodsAPI.index();
</script>

<template>
    <h2>{{ strip.section }} strip {{ strip.date }} <span class="small">{{ strip.until }} days left to close the
            set</span></h2>
    <div><img src="@/assets/sections.png" style="width:100%" /></div>
</template>