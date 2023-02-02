<script setup>
import { ref } from 'vue';
import GradeDistribution from '../components/GradeDistribution.vue';
import SetterMethods from '../api/resources/SetterMethods';
import { name, setter_code, sections, setter, setter_auth } from '../localStorage';

const button_data = ref({
    disabled: false,
    text: "link your setter code *"
})

async function link_setter_code(e) {
    button_data.value.disabled = true
    button_data.value.text = "working..."
    try {
        const answer = await SetterMethods.get(setter_code.value)
        setter_auth.value = answer.access_token;
        window.location.reload()
    } catch (error) {

    }
    button_data.value.disabled = false
    button_data.value.text = "link your setter code *"
}
</script>

<template>
    <div class="flex one">
        <div>
            <h2>Profile for {{ name }}</h2>
        </div>
        <div>
            <label for="name">Name</label>
            <input v-model="name" type="text" required name="name" placeholder="name" />
            <label>Frontpage modules</label>
            <label class="labelblock" for="calendar"><input type="checkbox" id="calendar" name="calendar"
                    value="calendar" v-model="sections.value" /><span class="checkable">calendar</span></label>
            <label class="labelblock" for="hours_popular"><input type="checkbox" id="hours_popular" name="hours_popular"
                    value="hours_popular" v-model="sections.value" /><span class="checkable">peak
                    hours</span></label>
            <label class="labelblock" for="strip"><input type="checkbox" id="strip" name="strip" value="strip"
                    v-model="sections.value" /><span class="checkable">strip
                    section</span></label>
            <label class="labelblock" for="problems"><input type="checkbox" id="problems" name="problems"
                    value="problems" v-model="sections.value" /><span class="checkable">problems</span></label>
            <label>Do you set problems?</label>
            <select v-model="setter" name="setter">
                <option value="no">no</option>
                <option value="yes">yes</option>
            </select>
        </div>
        <div v-if="setter.value == 'yes'">
            <GradeDistribution></GradeDistribution>
            <label for="setter_code">
                <h2>Setter code</h2>
            </label>
            <input v-model="setter_code.value" type="text" name="setter_code"
                placeholder="enter current code for 'grebrum'" />
            <p>status: <span v-if="setter_auth.value" class="green">setter code is linked successful</span><span v-else
                    class="orange">not linked</span></p>
            <button v-if="!setter_auth.value" :disabled="button_data.disabled" @click="link_setter_code">{{
                button_data.text
            }}</button>
            <p v-if="!setter_auth.value">* wait up to 15 seconds after clicking - status should be green</p>
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