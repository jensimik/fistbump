<script setup>
import ProblemsMethodsAPI from '../api/resources/ProblemsMethods.js';
import { filter_rp_grades, filter_rp_sections } from '../localStorage'
import { ref, onMounted, onBeforeUnmount } from 'vue';

const items = ref([]);
const online = ref(true);

// refresh function
const refresh = async () => {
    try {
        items.value = await ProblemsMethodsAPI.search({ grades: filter_rp_grades.value, sections: filter_rp_sections.value });
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
    <h2><router-link :to="{ name: 'problems' }">Recent Problems</router-link> <span class="small">(<a
                href="https://www.getstokt.com/">stökt</a> | lumi | probyg |
            fribyg) </span>
    </h2>
    <table v-if="online" class="primary">
        <tbody>
            <tr v-for="item in items" :key="item.id">
                <td class="time">-{{ item.days_back }}d</td>
                <td class="section"><span v-if="item.color" class="label" :class="item.color"
                        :title="'holds color ' + item.color">{{ item.section }}</span><span v-else>{{
                            item.section
                        }}</span></td>
                <td class="name"><span><router-link :to="{ name: 'problem', params: { id: item.id } }">{{
                    item.name
                }}</router-link></span></td>
                <td class="tdgrade"><span class="label grade" :class="item.grade_class">{{
                    item.grade
                }}</span></td>
            </tr>
        </tbody>
    </table>
    <div v-else>
        could not fetch data - are you online?
    </div>
</template>

<style scoped>
h2 {
    padding: 0;
}

td.time {
    text-align: center;
    width: 2.5em;
}

td.section {
    width: 2.5em;
}

td.tdgrade {
    text-align: center;
    width: 5em;
}

td.name {
    width: calc(100% - 10em);
}

td.name span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: block;
    display: inline-block;
    white-space: nowrap;
    position: relative;
    width: 100%;
    margin-right: -1000px;
    vertical-align: middle;
}

td {
    padding-right: 0.1em;
    padding-left: 0;
}

tr td:first-child {
    padding-left: 0.3em;
}

tr td:last-child {
    padding-right: 0.3em;
}

span.grade {
    width: 5em;
}

td.section {
    text-align: center;
}

span.label {
    margin-left: 0;
}
</style>