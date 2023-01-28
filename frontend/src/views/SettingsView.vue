<script setup>
import GradeDistribution from '../components/GradeDistribution.vue';
import router from '../router/index.js';
import useLocalStorage from '../useLocalStorage';

const data = {
    name: useLocalStorage("name", ""),
    setter_code: useLocalStorage("setter_code", ""),
    grade: useLocalStorage("grade", "5C-6A+"),
    sections: useLocalStorage("sections", ["calendar", "hours_popular", "strip", "problems"]),
    setter: useLocalStorage("setter", "no"),
};
</script>

<template>
    <div class="flex one">
        <div>
            <h2>Profile for {{ data.name }}</h2>
        </div>
        <div>
            <label for="name">Name</label>
            <input v-model="data.name.value" type="text" required name="name" placeholder="name" />
            <label for="grade">Grade</label>
            <select v-model="data.grade.value" name="grade">
                <option value="4-5A">Green range (4-5A)</option>
                <option value="5B-5B+">Yellow range (5B-5B+)</option>
                <option value="5C-6A+">Blue range (5C-6A+)</option>
                <option value="6B-6B+">Purple range (6B-6B+)</option>
                <option value="6C-6C+">Red range (6C-6C+)</option>
                <option value="7A-7A+">Brown range (7A-7A+)</option>
                <option value="7B-7C">Black range (7B-7C)</option>
                <option value="7C+-8C">Mytical white (7C+-8C)</option>
            </select>
            <label>Frontpage modules</label>
            <label class="labelblock" for="welcome"><input type="checkbox" id="welcome" name="welcome" value="welcome"
                    v-model="data.sections.value" /><span class="checkable">welcome message</span></label>
            <label class="labelblock" for="calendar"><input type="checkbox" id="calendar" name="calendar"
                    value="calendar" v-model="data.sections.value" /><span class="checkable">calendar</span></label>
            <label class="labelblock" for="hours_popular"><input type="checkbox" id="hours_popular" name="hours_popular"
                    value="hours_popular" v-model="data.sections.value" /><span class="checkable">peak
                    hours</span></label>
            <label class="labelblock" for="strip"><input type="checkbox" id="strip" name="strip" value="strip"
                    v-model="data.sections.value" /><span class="checkable">strip
                    section</span></label>
            <label class="labelblock" for="problems"><input type="checkbox" id="problems" name="problems"
                    value="problems" v-model="data.sections.value" /><span class="checkable">problems</span></label>
            <label>Do you set problems?</label>
            <select v-model="data.setter.value" name="setter">
                <option value="no">no</option>
                <option value="yes">yes</option>
            </select>
        </div>
        <div v-if="data.setter.value == 'yes'">
            <GradeDistribution></GradeDistribution>
            <label for="setter_code">
                <h2>Setter code</h2>
            </label>
            <input v-model="data.setter_code.value" type="text" name="setter_code"
                placeholder="leave empty if you are not setting problems" />
            <button @click="link_setter_code">link your setter code</button>
        </div>
    </div>
</template>


<style scoped>
button {
    width: 100%;
}

.labelblock {
    display: block;
}
</style>