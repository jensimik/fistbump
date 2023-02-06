<script setup>
import HoldStatsMethodsAPI from '../api/resources/HoldStatsMethods.js';
import { ref } from 'vue';

const data = ref({});
data.value = await HoldStatsMethodsAPI.index();
</script>

<template>
    <h2>Holds in use</h2>
    <div class="flex two">
        <div>Holds</div>
        <div class="right"><span class="label" :class="color" v-for="(c, color) in data.holds">{{
            c
        }}</span>
        </div>
        <div>
            Problems</div>
        <div class="right"><span class="label" :class="color" v-for="(c, color) in data.holds">{{
            c
        }}</span>
        </div>
    </div>
</template>

<style scoped>
div.right {
    text-align: right;
}
</style>