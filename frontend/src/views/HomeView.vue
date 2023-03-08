<script setup>
import Layout from '../components/Layout.vue';
import { RouterLink } from 'vue-router'
import RecentProblems from '../components/RecentProblems.vue';
import HoursPopular from '../components/HoursPopular.vue';
import Calendar from '../components/Calendar.vue';
import Strip from '../components/NextStrip.vue';
import { sections, setter_auth } from '../localStorage';
</script>

<template>
  <Layout>
    <template v-slot:menu>
      <router-link v-if="setter_auth" :to="{ name: 'add_problem' }" class="button">➕</router-link>
    </template>
    <template v-slot:content>
      <div>
        <Calendar v-if="sections.includes('calendar')"></Calendar>
        <HoursPopular v-if="sections.includes('hours_popular')"></HoursPopular>
        <Strip v-if="sections.includes('strip')"></Strip>
        <RecentProblems v-if="sections.includes('problems')"></RecentProblems>
      </div>
    </template>
  </Layout>
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