<script setup>
import { RouterLink, RouterView } from 'vue-router'
import addToHomeButton from './components/addToHomeScreen.vue';
import ReloadPrompt from './components/ReloadPrompt.vue';
import { setter_auth } from './localStorage';
</script>

<template>
  <div class="main">
    <nav class="imponent">
      <router-link :to="{ name: 'home' }" class="brand">
        <img class="logo" src="@/assets/fist.png" />
      </router-link>

      <div class="menu">
        <addToHomeButton></addToHomeButton>
        <router-link v-if="setter_auth" :to="{ name: 'add_problem' }" class="button">+problem</router-link>
        <router-link :to="{ name: 'settings' }" class="button">settings</router-link>
      </div>
    </nav>

    <div class="flex one">
      <div class="full paddypower"></div>
      <Suspense>
        <div id="content">
          <div>
            <RouterView />
          </div>
        </div>
        <template #fallback>
          <div>Loading...</div>
        </template>
      </Suspense>
    </div>
    <ReloadPrompt></ReloadPrompt>
  </div>
</template>

<style scoped>
#content div {
  padding: 0 0.15em;
}

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
  line-height: 1.5;
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

span.orange {
  background-color: #FF851B;
}

span.rainbow {
  background-image: linear-gradient(to left, #85144b, #FF4136, #B10DC9, #0074d9, #2ECC40, #FFDC00);
}
</style>