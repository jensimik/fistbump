<script setup>
import FeedMethodsAPI from '../api/resources/FeedMethods.js';
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
        case "6B":
            return "purple";
        case "6B+":
            return "purple";
        case "6C":
            return "red";
        case "6C+":
            return "red";
        case "7A":
            return "brown";
        case "7A+":
            return "brown";
        case "7B":
            return "black";
        case "7B+":
            return "black";
        case "7C":
            return "black";
        case "7C+":
            return "pink";
        case "8A":
            return "pink";
    }
}
const items = ref([]);
items.value = await FeedMethodsAPI.index();
</script>

<template>
    <h2>Problems <span class="small">(<a href="https://www.getstokt.com/">stökt</a>, bennehul2000, <router-link
                :to="{ name: 'addproblem' }">user-entry</router-link>)</span>
    </h2>
    <table class="primary">
        <tbody>
            <tr v-for="item in items">
                <td>-{{ item.days_back }}d</td>
                <td class="section">{{ item.section }}</td>
                <td class="name">{{ item.name }} </td>
                <td><span class="label" :style="{ backgroundColor: gradeToColor(item.grade) }">{{
                    item.grade
                }}</span></td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>
td.name {
    width: 75%;
}

td {
    padding-right: 0.15em;
    padding-left: 0;
}

tr td:first-child {
    padding-left: 0.3em;
}

tr td:last-child {
    padding-right: 0.3em;
}

/* td.section {
    padding-right: 0.15em;
} */

span.label {
    width: 3.5em;
}
</style>