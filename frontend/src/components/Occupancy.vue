<script setup>
import OccupancyMethodsAPI from '../api/resources/OccupancyMethods.js'
import { ref, onMounted, onBeforeUnmount } from 'vue'

const occupancy = ref({});
const online = ref(true);


// refresh function
const refresh = async () => {
    try {
        occupancy.value = await OccupancyMethodsAPI.index();
        online.value = true;
    } catch (error) {
        online.value = false;
    }
}

const visibilityChange = async () => {
    if (document.visibilityState === 'visible') {
        await refresh();
    }
}
const networkOnline = async () => {
    await refresh();
}
onMounted(async () => {
    await refresh();
    document.addEventListener('visibilitychange', visibilityChange);
    window.addEventListener('online', networkOnline);
})

onBeforeUnmount(async () => {
    document.removeEventListener('visibilitychange', visibilityChange);
    window.removeEventListener('online', networkOnline);
})
</script>

<template>
    <div v-if="online">
        <h2>Lockoff</h2>
        <div class="flex one">
            <div v-if="occupancy.currently < (occupancy.historical - 2)">💚 less busy than usual (<span :title="occupancy.currently + ' checkins last hour where the average is ' + occupancy.historical + ' for this hour/day'">curr {{ occupancy.currently }} avg {{ occupancy.historical }}</span>)</div>
            <div v-if="(occupancy.currently >= (occupancy.historical -2)) & (occupancy.currently <= (occupancy.historical + 2))">💛 average busyness (<span :title="occupancy.currently + ' checkins last hour where the average is ' + occupancy.historical + ' for this hour/day'">curr {{ occupancy.currently }} avg {{ occupancy.historical }}</span>)</div>
            <div v-if="occupancy.currently > (occupancy.historical + 2)">🔥 more busy than usual (<span :title="occupancy.currently + ' checkins last hour where the average is ' + occupancy.historical + ' for this hour/day'">curr {{ occupancy.currently }} avg {{ occupancy.historical }}</span>)</div>
        </div>
    </div>
</template>

<style scoped>
</style>