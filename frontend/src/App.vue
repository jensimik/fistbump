<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="flex main">
    <div class="full">
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
    </div>

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
  position: relative;
  margin: 0;
  box-shadow: none;
  border-bottom: 4px dotted #dfdfdf;
}
</style>
<style>
table.primary {
  width: 100%;
}
</style>