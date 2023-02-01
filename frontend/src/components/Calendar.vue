<script setup>
import CalendarMethodsAPI from '../api/resources/CalendarMethods.js'
import HourMethodsAPI from '../api/resources/HourMethods.js'
import { ref, onMounted, onBeforeUnmount } from 'vue'

const items = ref([])
const hours = ref({})

// refresh function
const refresh = async () => {
    items.value = await CalendarMethodsAPI.index()
    hours.value = await HourMethodsAPI.index()
}

const visibilityChange = async () => {
    if (document.visibilityState === 'visible') {
        await refresh()
    }
}
onMounted(async () => {
    await refresh();
    document.addEventListener('visibilitychange', visibilityChange)
})

onBeforeUnmount(async () => {
    document.removeEventListener('visibilitychange', visibilityChange)
})

</script>

<template>
    <h2>Calendar <span class="small">(<a href="https://nkk.klub-modul.dk/cms/Activity.aspx">klubmodul</a> | <a
                href="https://kulturogfritidn.kk.dk/noerrebrohallen">nørrebrohallen</a>)</span></h2>

    <div class="flex two">
        <div class="third">{{ hours.hours_today }}</div>
        <div class="two-third">hours today ({{ hours.today }})</div>
    </div>

    <div class="flex two" v-for="item in items" v-if="items.length">
        <div class="third">{{ item.time }}</div>
        <div class="two-third">{{ item.title }}</div>
    </div>
    <div v-else class="flex">
        <div class="two-third off-third">empty klubmodul calendar</div>
    </div>
</template>