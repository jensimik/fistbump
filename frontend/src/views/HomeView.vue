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
        <p class="deprecate">⚠️ fistbump is closing down soon (sometime in june). it proved too difficult to get people to add problems to the app manually (and it is not sustainable for me to keep adding all the problems).</p>
        <p>📊 i made a snapshot of statistics end of february from fistbump-data - i think quite interesting data:</p>
        <p>🖍️ on average 2.1 problems of each hold color per section (and by color: blue 2.6, red 2.4, green 2.4, black 2.4, purple 2.2, yellow 2.0, white 2.0, orange 1.6, brown 1.2) orange is a less popular bigger series, and white and brown are popular smaller series.</p>
        <p>👷 93 problems in the gym on all sections (probyg about 40% and fribyg about 60% - where probyg had 3 sections and fribyg 2 sections)</p>
        <p>🤪 70 problems in stökt in the same period (~5 weeks)</p>
        <p>💪 160 problems in 5 weeks is 32 per week or 10 problems per session if you climb three times a week </p>
        <p>👷 probyg share of grades: 6/8 green (75%), 8/15 yellow (50%), 7/24 blue (30%), 7/17 purple (41%), 5/20 red (25%), 5/10 brown/black (50%) - it is a myth that fribyg do not build yellows/blues 🙈</p>
        <p>🪑 sitstarts: fribyg 56% sitstarts (35 of 63 problems), probyg 0% sitstarts (0 of 24 problems)</p>
        <p>⛰️ topouts: fribyg 54% topouts (34 of 63 problems), probyg 4% topouts (1 of 24 problems)</p>
        <p style="text-align:right;">🤜🤛 JD</p>
        <Calendar v-if="sections.includes('calendar')"></Calendar>
        <HoursPopular v-if="sections.includes('hours_popular')"></HoursPopular>
        <Strip v-if="sections.includes('strip')"></Strip>
        <RecentProblems v-if="sections.includes('problems')"></RecentProblems>
      </div>
    </template>
  </Layout>
</template>

<style scoped>
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