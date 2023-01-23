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
                <option value="5B">Yellow soft (5b)</option>
                <option value="5B+">Yellow hard (5b+)</option>
                <option value="5B-5B+">Yellow range (5b-5b+)</option>
                <option value="5C">Blue soft (5c)</option>
                <option value="6A">Blue medium (6a)</option>
                <option value="6A+">Blue hard (6a+)</option>
                <option value="5C-6A+">Blue range (5c-6a+)</option>
                <option value="6B">Purple soft (6b)</option>
                <option value="6B+">Purple hard (6b+)</option>
                <option value="6B-6B+">Purple range (6b-6b+)</option>
                <option value="6C">Red soft (6c)</option>
                <option value="6C+">Red hard (6c+)</option>
                <option value="6C-6C+">Red range (6c-6c+)</option>
                <option value="7A">Brown soft (7a)</option>
                <option value="7A+">Brown hard (7a+)</option>
                <option value="7A-7A+">Brown range (7a-7a+)</option>
                <option value="7B">Black soft (7b)</option>
                <option value="7B+">Black medium (7b+)</option>
                <option value="7C">Black hard (7c)</option>
                <option value="7B-7C">Black range (7b-7c)</option>
                <option value="7C+-8C">Mytical white (7c+-8c)</option>
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