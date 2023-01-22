<script setup>
import HourMethodsAPI from '../api/resources/HourMethods.js';
import { ref } from 'vue';

const hours = ref({});
hours.value = await HourMethodsAPI.index();
</script>

<template>
    <h2>Hours</h2>
    <div>{{ hours.hours_today }}</div>

    <!--
    <table class="primary">
        <thead>
            <tr>
                <th colspan="2">Hours</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Today</td>
                <td>{{ hours.hours_today }}</td>
            </tr>
            <tr>
                <td>Tomorrow</td>
                <td>{{ hours.hours_tomorrow }}</td>
            </tr>
        </tbody>
    </table>
-->
</template>