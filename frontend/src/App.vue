<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
      <Suspense>
        <div>
          <RouterView />
        </div>
        <template #fallback>
          <div>Loading...</div>
        </template>
      </Suspense>
</template>

<style>
body {
  background-color: #efefef;
  line-height: 1.5;
}

.turquoise {
  background-color: #39CCCC;
  color: #111111;
}

.yellow {
  background-color: #FFDC00;
  color: #111111;
}

.green {
  background-color: #2ECC40;
}

.blue {
  background-color: #0074d9;
}

.purple {
  background-color: #B10DC9;
}

.red {
  background-color: #FF4136;
}

.brown {
  background-color: #85144b;
}

.black {
  background-color: #111111;
}

.white {
  background-color: #fff;
  color: #111111;
}

.orange {
  background-color: #FF851B;
}

.rainbow {
  background-image: linear-gradient(to left, #85144b, #FF4136, #B10DC9, #0074d9, #2ECC40);
}
</style>