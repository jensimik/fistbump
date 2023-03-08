<script setup>
import { RouterLink } from 'vue-router'
import addToHomeButton from './addToHomeScreen.vue';
import ReloadPrompt from './ReloadPrompt.vue';
import { setter_auth } from '../localStorage';
</script>

<template>
  <div class="main">
    <nav class="imponent">
      <router-link :to="{ name: 'home' }" class="brand">
        <img class="logo" src="@/assets/fist.png" />
      </router-link>

      <div class="menu">
        <addToHomeButton></addToHomeButton>
        <slot name="menu"></slot>
        <router-link :to="{ name: 'settings' }" class="button">⚙️</router-link>
      </div>
    </nav>

    <div class="flex one">
      <div class="full paddypower"></div>
        <div id="content">
          <div>
            <slot name="content"></slot>
          </div>
        </div>
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