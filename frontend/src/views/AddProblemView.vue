<script setup>
import FeedMethodsAPI from '../api/resources/FeedMethods.js';
import router from '../router/index.js';
import { ref } from 'vue';

const data = ref({
  name: "",
  grade: "6a",
  section: "S1",
});

async function add(e) {
  await FeedMethodsAPI.store(data.value)
  router.push({ name: 'home' })
}

</script>

<template>
  <div class="flex one">
    <div>
      <h2>Add problem</h2>
    </div>
    <div>
      Awesome with a new problem 💪 let's add it
    </div>
    <div>
      <label for="name">Name</label>
      <input v-model="data.name" type="text" required name="name"
        placeholder="give it a good name and tag the tape too" />
      <label for="grade">Grade</label>
      <select v-model="data.grade" name="grade">
        <option value="let">Green (let)</option>
        <option value="5b">Yellow soft (5b)</option>
        <option value="5b+">Yellow hard (5b+)</option>
        <option value="5b-5b+">Yellow range (5b-5b+)</option>
        <option value="5c">Blue soft (5c)</option>
        <option value="6a">Blue medium (6a)</option>
        <option value="6a+">Blue hard (6a+)</option>
        <option value="5c-6a+">Blue range (5c-6a+)</option>
        <option value="6b">Purple soft (6b)</option>
        <option value="6b+">Purple hard (6b+)</option>
        <option value="6b-6b+">Purple range (6b-6b+)</option>
        <option value="6c">Red soft (6c)</option>
        <option value="6c+">Red hard (6c+)</option>
        <option value="6c-6c+">Red range (6c-6c+)</option>
        <option value="7a">Brown soft (7a)</option>
        <option value="7a+">Brown hard (7a+)</option>
        <option value="7a-7a+">Brown range (7a-7a+)</option>
        <option value="7b">Black soft (7b)</option>
        <option value="7b+">Black medium (7b+)</option>
        <option value="7c">Black hard (7c)</option>
        <option value="7b-7c">Black range (7b-7c)</option>
        <option value="7c+-8c">Mytical white (7c+-8c)</option>
      </select>
      <label for="section">Section</label>
      <select v-model="data.section" name="section">
        <option value="S1">Section1</option>
        <option value="S2">Section2</option>
        <option value="S3">Section3</option>
        <option value="S4">Section4</option>
        <option value="S5">Section5</option>
      </select>
      <button class="button" @click="add">add</button>
    </div>
  </div>
</template>