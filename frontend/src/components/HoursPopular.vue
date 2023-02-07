<script setup>
import HoursPopularMethodsAPI from '../api/resources/HoursPopularMethods.js'
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { GChart } from 'vue-google-charts'

const type = 'ColumnChart'

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

const hours = ref([]);
const online = ref(true);

// refresh function
const refresh = async () => {
    try {
        hours.value = [["Hour", "People"]].concat(await HoursPopularMethodsAPI.index());
        online.value = true;
    } catch (error) {
        online.value = false;
        hours.value = [];
    }
}

const visibilityChange = async () => {
    if (document.visibilityState === 'visible') {
        await refresh()
    }
}
onMounted(async () => {
    await refresh()
    document.addEventListener('visibilitychange', visibilityChange)
})

onBeforeUnmount(async () => {
    document.removeEventListener('visibilitychange', visibilityChange)
})

</script>

<template>
    <h2>Peak hours <span class="small">(<a
                href="https://www.google.com/maps/place/N%C3%B8rrebro+Klatreklub/@55.699755,12.54276,17z/data=!3m1!4b1!4m5!3m4!1s0x4652524dad58ebed:0x9717e97520fbdbbb!8m2!3d55.699755!4d12.54276">google-maps
                estimate</a>)</span></h2>
    <div v-if="online">
        <GChart id="ccc" :data="hours" :options="options" :type="type"></GChart>
    </div>
    <div v-else>could not fetch data - are you online?</div>
</template>

<style scoped>
#ccc {
    height: 6em;
}
</style>