<script setup>
import Feed from '../components/Feed.vue'
// import Hours from '../components/Hour.vue'
import HoursPopular from '../components/HoursPopular.vue'
import Calendar from '../components/Calendar.vue'
</script>

<template>
  <!-- <Hours></Hours> -->
  <Calendar></Calendar>
  <HoursPopular></HoursPopular>
  <h2>Section4 strip 4 feb <span class="small">X days left to close the set</span></h2>
  <div><img src="@/assets/sections.png" style="width:100%" /></div>
  <Feed></Feed>
</template>