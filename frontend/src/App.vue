<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue';
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
  /* max-width: 800px; */
  /* margin-left: auto; */
  /* margin-right: auto; */
  box-shadow: none;
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