<script setup>
import CalendarMethodsAPI from '../api/resources/CalendarMethods.js';
import HourMethodsAPI from '../api/resources/HourMethods.js';
import { ref, onMounted, onBeforeUnmount } from 'vue';

const calendar = ref([]);
const hours = ref({});
const online_calendar = ref(true);
const online_hours = ref(true);

// refresh function
const refresh = async () => {
    try {
        calendar.value = await CalendarMethodsAPI.index();
        online_calendar.value = true;
    } catch (error) {
        calendar.value = [{ time: "error", title: "failed to fetch - are you online?" }];
        online_calendar.value = false;
    }
    try {
        hours.value = await HourMethodsAPI.index();
        online_hours.value = true;
    } catch (error) {
        hours.value = { hours_today: "error", today: "error" }
        online_hours.value = false;
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
    <h2>Today <span class="small">(<a href="https://nkk.klub-modul.dk/cms/Activity.aspx">klubmodul</a> | <a
                href="https://kulturogfritidn.kk.dk/noerrebrohallen">nørrebrohallen</a>)</span></h2>

    <div v-if="online_hours" class="flex two">
        <div class="third">{{ hours.hours_today }}</div>
        <div class="two-third">hours today ({{ hours.today }})</div>
    </div>
    <div v-else>
        error fetching data - are you online?
    </div>

    <div v-if="online_calendar">
        <div class="flex two" v-for="item in calendar" v-if="calendar.length">
            <div class="third">{{ item.time }}</div>
            <div class="two-third">{{ item.title }}</div>
        </div>
        <div v-else class="flex">
            <div class="two-third off-third">empty klubmodul calendar</div>
        </div>
    </div>
    <div v-else>
        error fetching data - are you online?
    </div>
</template>