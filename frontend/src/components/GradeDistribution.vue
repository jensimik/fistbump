<script setup>
import GradeDistributionMethodsAPI from '../api/resources/GradeDistributionMethods.js';
import { GChart } from 'vue-google-charts';
import { ref } from 'vue';

const type = 'BarChart';

const options = {
    width: '100%',
    height: '100%',
    chartArea: { left: '0', top: 0, width: "100%", height: '100%' },
    bar: { groupWidth: '50%' },
    isStacked: "percent",
    legend: { position: "none" },
    series: {
        0: {
            color: '#2ECC40',
        },
        1: {
            color: '#FFDC00',
        },
        2: {
            color: '#0074d9',
        },
        3: {
            color: '#B10DC9',
        },
        4: {
            color: '#FF4136',
        },
        5: {
            color: '#85144b',
        },
        6: {
            color: '#111111'
        },
        7: {
            color: '#fff'
        }
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
const data_boulder = [
    ['Type', 'green', { role: 'annotation' }, 'yellow', { role: 'annotation' }, 'blue', { role: 'annotation' }, 'purple', { role: 'annotation' }, 'red', { role: 'annotation' }, 'brown', { role: 'annotation' }, 'black', { role: 'annotation' }, 'white', { role: 'annotation' }],
    ['Boulder', distribution.value.boulder.green, distribution.value.boulder.green, distribution.value.boulder.yellow, distribution.value.boulder.yellow, distribution.value.boulder.blue, distribution.value.boulder.blue, distribution.value.boulder.purple, distribution.value.boulder.purple, distribution.value.boulder.red, distribution.value.boulder.red, distribution.value.boulder.brown, distribution.value.boulder.brown, distribution.value.boulder.black, distribution.value.boulder.black, distribution.value.boulder.white, distribution.value.boulder.white],
];
const data_stokt = [
    ['Type', 'green', { role: 'annotation' }, 'yellow', { role: 'annotation' }, 'blue', { role: 'annotation' }, 'purple', { role: 'annotation' }, 'red', { role: 'annotation' }, 'brown', { role: 'annotation' }, 'black', { role: 'annotation' }, 'white', { role: 'annotation' }],
    ['Stökt', distribution.value.stokt.green, distribution.value.stokt.green, distribution.value.stokt.yellow, distribution.value.stokt.yellow, distribution.value.stokt.blue, distribution.value.stokt.blue, distribution.value.stokt.purple, distribution.value.stokt.purple, distribution.value.stokt.red, distribution.value.stokt.red, distribution.value.stokt.brown, distribution.value.stokt.brown, distribution.value.stokt.black, distribution.value.stokt.black, distribution.value.stokt.white, distribution.value.stokt.white],
];
</script>

<template>
    <h2>Grade distribution <span class="small">()</span>
    </h2>
    <h3>Boulder</h3>
    <GChart class="cc" :data="data_boulder" :options="options" :type="type"></GChart>
    <h3>Stökt</h3>
    <GChart class="cc" :data="data_stokt" :options="options" :type="type"></GChart>
</template>

<style scoped>
.cc {
    height: 4em;
}

h3 {
    margin: 0;
    padding: 0;
}
</style>