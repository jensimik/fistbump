<script setup>
import GradeDistributionMethodsAPI from '../api/resources/GradeDistributionMethods.js';
import { GChart } from 'vue-google-charts';
import { ref } from 'vue';

const type = 'ColumnChart';

const options = {
    chartArea: { width: '100%' },
    isStacked: "percent",
    legend: { position: "none" },
    series: {
        0: {
            color: '#0074d9'
        },
    },
    backgroundColor: 'transparent',
    hAxis: {
        gridlines: {
            interval: 0,
            color: 'none',
        },
        baselineColor: 'none',
    },
    vAxis: {
        gridlines: {
            interval: 0,
            color: 'none',
        },
        baselineColor: 'none',
    },
};


const distribution = ref({});
distribution.value = await GradeDistributionMethodsAPI.index();

const data = [
    ['Type', 'green', 'yellow', 'blue', 'purple', 'red', 'brown', 'black', 'white', { role: 'annotation' }],
    ['Boulder', distribution.value.boulder.green, distribution.value.boulder.yellow, distribution.value.boulder.blue, distribution.value.boulder.purple, distribution.value.boulder.red, distribution.value.boulder.brown, distribution.value.boulder.black, distribution.value.boulder.white],
    ['Stökt', distribution.value.stokt.green, distribution.value.stokt.yellow, distribution.value.stokt.blue, distribution.value.stokt.purple, distribution.value.stokt.red, distribution.value.stokt.brown, distribution.value.stokt.black, distribution.value.stokt.white]
]

console.log(distribution.value)
</script>

<template>
    <h2>Grade distribution <span class="small">()</span>
    </h2>
    <GChart id="ccc" :data="data" :options="options" :type="type"></GChart>
</template>