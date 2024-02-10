<script setup>
import Layout from '../components/Layout.vue';
import { RouterLink } from 'vue-router'
import RecentProblems from '../components/RecentProblems.vue';
//import HoursPopular from '../components/HoursPopular.vue';
import Calendar from '../components/Calendar.vue';
import Strip from '../components/NextStrip.vue';
import Occupancy from '../components/Occupancy.vue';
import { sections, setter_auth } from '../localStorage';
</script>

<template>
  <Layout>
    <template v-slot:menu>
<!--      <router-link v-if="setter_auth" :to="{ name: 'add_problem' }" class="button">➕</router-link>-->
    </template>
    <template v-slot:content>
      <div>
        <Calendar v-if="sections.includes('calendar')"></Calendar>
        <Occupancy></Occupancy>
        <Strip v-if="sections.includes('strip')"></Strip>
        <RecentProblems></RecentProblems>
        <!-- <HoursPopular v-if="false"></HoursPopular> -->
        <div class="hidden">
          <p class="deprecate">⚠️ fistbump is closing down ⚠️</p>
          <p>it proved too difficult to get people to add problems to the app manually (and it is not sustainable for me to keep adding all the problems).</p>
          <p style="text-align:right;">🤜🤛 JD</p>
        </div>
      </div>
    </template>
  </Layout>
</template>

<style scoped>
.hidden {
  display: none;
}
.deprecate {
  color: red;
}
.welcome {
  background-color: #7FDBFF;
  padding: 1.5em;
}

dt {
  text-decoration: underline;
}
</style>