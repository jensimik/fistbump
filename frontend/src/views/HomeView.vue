<script setup>
import { ref } from 'vue';
import Feed from '../components/Feed.vue'
import HoursPopular from '../components/HoursPopular.vue'
import Calendar from '../components/Calendar.vue'
import Strip from '../components/NextStrip.vue'
import GradeDistribution from '../components/GradeDistribution.vue'


const componentKey = ref(0);

const forceRerender = () => {
  componentKey.value += 1;
};

// refresh on visibilitychange (switching to the app)
window.addEventListener('visibilitychange', function () {
  if (document.visibilityState === 'visible') {
    componentKey.value += 1;
  }
});

</script>

<template>
  <div :key="componentKey">
    <Calendar></Calendar>
    <HoursPopular></HoursPopular>
    <Strip></Strip>
    <Feed></Feed>
    <GradeDistribution></GradeDistribution>
  </div>
</template>