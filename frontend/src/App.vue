<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue';
import addToHomeButton from './components/addToHomeScreen.vue';

const componentKey = ref(0);

const forceRerender = () => {
  componentKey.value += 1;
};
</script>

<template>
  <div class="main">

    <nav class="imponent">
      <router-link :to="{ name: 'home' }" class="brand">
        <img class="logo" src="@/assets/fist.png" />
      </router-link>

      <div class="menu">
        <addToHomeButton></addToHomeButton>
        <button class="button" @click="forceRerender">refresh</button>
        <router-link :to="{ name: 'addproblem' }" class="button">+problem</router-link>
      </div>
    </nav>

    <div class="flex one" :key="componentKey">
      <div class="full paddypower"></div>
      <Suspense>
        <div>
          <RouterView />
        </div>
        <template #fallback>
          <div>Loading...</div>
        </template>
      </Suspense>
    </div>
  </div>
</template>

<style scoped>
div.main {
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

nav.imponent {
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: none;
  background-color: #efefef;
  border-bottom: 4px dotted #dfdfdf;
}

div.paddypower {
  padding-top: 2.5em;
}

.logo {
  height: 4.5em;
}

a.brand {
  padding-left: 0;
}
</style>
<style>
table.primary {
  width: 100%;
}

span.small {
  font-size: 0.3em;
}

h2 {
  padding-bottom: 0.2em;
}
</style>
<style>
body {
  background-color: #efefef;
}

span.turquoise {
  background-color: #39CCCC;
  color: #111111;
}

span.yellow {
  background-color: #FFDC00;
  color: #111111;
}

span.green {
  background-color: #2ECC40;
}

span.blue {
  background-color: #0074d9;
}

span.purple {
  background-color: #B10DC9;
}

span.red {
  background-color: #FF4136;
}

span.brown {
  background-color: #85144b;
}

span.black {
  background-color: #111111;
}

span.white {
  background-color: #fff;
  color: #111111;
}
</style>