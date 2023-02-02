<script setup>
import RecentProblems from '../components/RecentProblems.vue';
import HoursPopular from '../components/HoursPopular.vue';
import Calendar from '../components/Calendar.vue';
import Strip from '../components/NextStrip.vue';
import { sections } from '../localStorage';

</script>

<template>
  <div>
    <Calendar v-if="sections.includes('calendar')"></Calendar>
    <HoursPopular v-if="sections.includes('hours_popular')"></HoursPopular>
    <Strip v-if="sections.includes('strip')"></Strip>
    <RecentProblems v-if="sections.includes('problems')"></RecentProblems>
  </div>
</template>

<style scoped>
.welcome {
  background-color: #7FDBFF;
  padding: 1.5em;
}

dt {
  text-decoration: underline;
}
</style>