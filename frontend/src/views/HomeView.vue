<script setup>
import Feed from '../components/Feed.vue'
import HoursPopular from '../components/HoursPopular.vue'
import Calendar from '../components/Calendar.vue'
import Strip from '../components/NextStrip.vue'
import GradeDistribution from '../components/GradeDistribution.vue'
</script>

<template>
  <Calendar></Calendar>
  <HoursPopular></HoursPopular>
  <Strip></Strip>
  <Feed></Feed>
  <GradeDistribution></GradeDistribution>
</template>