<script setup>
import HoursPopularMethodsAPI from '../api/resources/HoursPopularMethods.js';
import { ref } from 'vue';
import { GChart } from 'vue-google-charts';


const type = 'ColumnChart';

const options = {
    chartArea: { width: '100%' },
    // width: 800,
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
console.log(hours.value);
</script>

<template>
    <table class="primary">
        <thead>
            <tr>
                <th colspan="2">Gym load</th>
            </tr>
        </thead>
        <tbody>
            <!--
            <tr>
                <td>Currently</td>
                <td>15</td>
            </tr>

-->
            <tr>
                <td>Today</td>
                <td class="cc">
                    <GChart id="ccc" :data="hours" :options="options" :type="type"></GChart>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>
td.cc {
    width: 100%;
}

#ccc {
    height: 6em;
}
</style>