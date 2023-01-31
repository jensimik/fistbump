<script setup>
import ProblemsMethodsAPI from '../api/resources/ProblemsMethods.js';
import { ref } from 'vue';

const items = ref([]);

// refresh function
async function refresh() {
    items.value = await ProblemsMethodsAPI.index();
}

await refresh();

// refresh on visibilitychange (switching to the app)
window.addEventListener('visibilitychange', async () => {
    if (document.visibilityState === 'visible') {
        await refresh();
    }
});
</script>

<template>
    <h2>Problems <span class="small">(<a href="https://www.getstokt.com/">stökt</a> | lumi | probyg | fribyg)</span>
    </h2>
    <table class="primary">
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