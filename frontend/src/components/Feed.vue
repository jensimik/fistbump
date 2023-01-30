<script setup>
import FeedMethodsAPI from '../api/resources/FeedMethods.js';
import formatDistanceToNowStrict from 'date-fns/formatDistanceToNowStrict'
import parseISO from 'date-fns/parseISO'
import { ref } from 'vue';

function gradeToColor(grade) {
    switch (grade.toUpperCase()) {
        case "?":
            return "turquoise";
        case "4":
            return "green";
        case "let":
            return "green";
        case "5+":
            return "orange";
        case "5B":
            return "orange";
        case "5B+":
            return "orange";
        case "5B-5B+":
            return "orange";
        case "5C":
            return "blue";
        case "5C+":
            return "blue";
        case "6A":
            return "blue";
        case "6A+":
            return "blue";
        case "5C-6A+":
            return "blue";
        case "6B":
            return "purple";
        case "6B+":
            return "purple";
        case "6B-6B+":
            return "purple";
        case "6C":
            return "red";
        case "6C+":
            return "red";
        case "6C-6C+":
            return "red";
        case "7A":
            return "brown";
        case "7A+":
            return "brown";
        case "7A-7A+":
            return "brown";
        case "7B":
            return "black";
        case "7B+":
            return "black";
        case "7C":
            return "black";
        case "7B-7C":
            return "black";
        case "7C+":
            return "pink";
        case "8A":
            return "pink";
        case "7C+-8C":
            return "pink";
    }
}
const items = ref([]);

// refresh function
async function refresh() {
    items.value = await FeedMethodsAPI.index();
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
                <td class="time">-{{ formatDistanceToNowStrict(parseISO(item.created)) }}</td>
                <td class="section"><span v-if="item.color" class="label" :class="item.color"
                        :title="'holds color ' + item.color">{{ item.section }}</span><span v-else>{{
                            item.section
                        }}</span></td>
                <td class="name"><router-link :to="{ name: 'problem', params: { id: item.id } }">{{
                    item.name
                }}</router-link></td>
                <td><span class="label grade" :class="item.grade_class">{{
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
    font-size: 0.5em;
}

td.name {
    width: 72%;
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