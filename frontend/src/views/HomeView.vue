<script setup>
import { ref } from 'vue';
import Feed from '../components/Feed.vue'
import HoursPopular from '../components/HoursPopular.vue'
import Calendar from '../components/Calendar.vue'
import Strip from '../components/NextStrip.vue'
import useLocalStorage from '../useLocalStorage';

const sections = useLocalStorage("sections", ["welcome", "calendar", "peak_hours", "strip", "problems"]);

async function dismiss(e) {
  const temp = sections.value;
  const index = temp.indexOf("welcome");
  temp.splice(index, 1);
  sections.value = temp
}

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
    <div v-if="sections.includes('welcome')" class="welcome">
      <h1>Nice to see you here 👊💪</h1>
      <p>This app is made to give you all the information for your daily NKK routine - check out what is happening while
        you are still at the couch/office 🛋️ anything new to climb? or should i set a new problem? 🪛</p>
      <dl>
        <dt>Navigation help</dt>
        <dd>⬆️ you can always click the 🤜🤛 icon in the top menu to return to the frontpage</dd>
        <dd>↗️ In settings you can configure your name, grade, and which modules to show on the frontpage</dd>
        <dd>⬇️ In the image showing the sections you can click the section name to get a section-view of problems on
          that section (try to click on S4)</dd>
        <dd>⬇️ In the problems list you can click on the name of a problem to view it</dd>
        <dt>Information in the app</dt>
        <dd>
          <dl>
            <dt>Calendar</dt>
            <dd>Todays opening hours and if there is anything in the calendar for today on klubmodul</dd>
            <dt>Peak hours</dt>
            <dd>How full the gym usually is today each hour 🐒🐒🐒🐒🐒</dd>
            <dt>Section overview</dt>
            <dd>Overview of the sections and which section will be stripped next (and how many days left to close the
              set).
              You can also click the section names to get a view of problems on that section.</dd>
            <dt>Problems</dt>
            <dd>List of most recent problems in the gym (both Stökt, boulder and Lumi)</dd>
            <dd>First column is how old the problem is (-Xd day sold)</dd>
            <dd>second column is which section it is on (and indicator of which color the holds are)</dd>
            <dd>third column is the name of the problem</dd>
            <dd>fourth column the grade (click on the name to get more information and an image of the problem)</dd>
          </dl>
        </dd>
        <dt>📱 Install</dt>
        <dd>You can "install" this webpage as an app on your mobile very easy (iphone/android)</dd>
        <dd>
          <dl>
            <dt>Iphone</dt>
            <dd>1) open this website in safari</dd>
            <dd>2) press 'share' icon</dd>
            <dd>3) 'add to homescreen'</dd>
            <dt>Android</dt>
            <dd>1) open this website in chrome</dd>
            <dd>2) tap 'install'</dd>
            <dd>3) follow instructions</dd>
          </dl>
        </dd>
      </dl>
      <button @click="dismiss">dismiss this welcome message</button>
    </div>
    <Calendar v-if="sections.includes('calendar')"></Calendar>
    <HoursPopular v-if="sections.includes('hours_popular')"></HoursPopular>
    <Strip v-if="sections.includes('strip')"></Strip>
    <Feed v-if="sections.includes('problems')"></Feed>
  </div>
</template>

<style scoped>
.welcome {
  background-color: #7FDBFF;
  padding: 1.5em;
}

dt {
  text-decoration: underline;
}
</style>