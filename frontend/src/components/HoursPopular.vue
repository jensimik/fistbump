<script setup>
import HoursPopularMethodsAPI from '../api/resources/HoursPopularMethods.js';
import { ref } from 'vue';
import { GChart } from 'vue-google-charts';


const type = 'ColumnChart';

const options = {
    chartArea: { width: '100%' },
    legend: { position: "none" },
    series: {
        0: {
            color: '#0074d9'
        },
    },
    backgroundColor: 'transparent',
    hAxis: {
        ticks: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
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

const hours = ref({});
hours.value = [["Hour", "People"]].concat(await HoursPopularMethodsAPI.index());
</script>

<template>
    <h2>Gym load</h2>
    <div>
        <GChart id="ccc" :data="hours" :options="options" :type="type"></GChart>
    </div>
</template>

<style scoped>
#ccc {
    height: 6em;
}
</style>