<script setup>
import Feed from '../components/Feed.vue'
import Hours from '../components/Hour.vue'
import HoursPopular from '../components/HoursPopular.vue'
import Calendar from '../components/Calendar.vue'
</script>

<template>
  <main>
    <Suspense>
      <main class="flexet">
        <Hours></Hours>
        <Calendar></Calendar>
        <HoursPopular></HoursPopular>
        <Feed></Feed>
      </main>
      <template #fallback>
        <div>Loading...</div>
      </template>
    </Suspense>
  </main>
</template>


<style scoped>
main {
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

table.primary {
  width: 100%;
}
</style>