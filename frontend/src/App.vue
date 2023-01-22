<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <nav class="imponent">
    <a href="#" class="brand">
      <img class="logo" src="@/assets/fist.png" />
      <span></span>
    </a>

    <!-- responsive-->
    <input id="bmenub" type="checkbox" class="show">
    <label for="bmenub" class="burger pseudo button">&#8801;</label>

    <div class="menu">
      <router-link :to="{ name: 'home' }" class="pseudo button icon-picture">Home</router-link>
      <router-link :to="{ name: 'about' }" class="button icon-puzzle">+problem</router-link>
    </div>
  </nav>

  <div class="flex main">
    <div class="full paddypower"></div>
    <RouterView />
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
</style>