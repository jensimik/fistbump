<script setup>
import HoldStatsMethodsAPI from '../api/resources/HoldStatsMethods.js';
import { ref } from 'vue';

const data = ref({});
data.value = await HoldStatsMethodsAPI.index();
</script>

<template>
    <h2>Holds color stats</h2>
    <div class="flex two">
        <div>Holds in use by color</div>
        <div class="right"><span class="label" :class="color" v-for="(c, color) in data.holds">{{
            c
        }}</span>
        </div>
        <div>
            Problems by hold color</div>
        <div class="right"><span class="label" :class="color" v-for="(c, color) in data.problems">{{
            c
        }}</span>
        </div>
    </div>
</template>

<style scoped>
div.right {
    text-align: right;
}

span.label {
    margin-left: 0;
}
</style>