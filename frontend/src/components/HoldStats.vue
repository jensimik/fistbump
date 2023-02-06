<script setup>
import HoldStatsMethodsAPI from '../api/resources/HoldStatsMethods.js';
import { ref } from 'vue';

const data = ref({});
data.value = await HoldStatsMethodsAPI.index();
</script>

<template>
    <h2>Stats by hold color</h2>
    <div class="flex two">
        <div class="third">Holds</div>
        <div class="two-third right"><span class="label" :class="c[0]" v-for="c in data.holds">{{
            c[1]
        }}</span>
        </div>
        <div class="third">Problems</div>
        <div class="two-third right"><span class="label" :class="c[0]" v-for="c in data.problems">{{
            c[1]
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