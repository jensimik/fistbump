<script setup>
import { ref } from 'vue';
import SetterMethods from '../api/resources/SetterMethods';
import { name, setter_code, sections, setter, setter_auth, filter_rp_grades, filter_rp_sections } from '../localStorage';

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
                    value="calendar" v-model="sections" /><span class="checkable">calendar</span></label>
            <label class="labelblock" for="hours_popular"><input type="checkbox" id="hours_popular" name="hours_popular"
                    value="hours_popular" v-model="sections" /><span class="checkable">peak
                    hours</span></label>
            <label class="labelblock" for="strip"><input type="checkbox" id="strip" name="strip" value="strip"
                    v-model="sections" /><span class="checkable">strip
                    section</span></label>
            <label class="labelblock" for="problems"><input type="checkbox" id="problems" name="problems"
                    value="problems" v-model="sections" /><span class="checkable">problems</span></label>
            <label>Recent problems filter</label>
            <div class="search_options">
                <label><input type="checkbox" name="B" value="B" v-model="filter_rp_sections" /><span
                        class="toggle button" :class="{
                            fade_button: !filter_rp_sections.includes('B')
                        }">Boulder</span></label>
                <label><input type="checkbox" name="Ö" value="Ö" v-model="filter_rp_sections" /><span
                        class="toggle button" :class="{
                            fade_button: !filter_rp_sections.includes('Ö')
                        }">Stökt</span></label>
            </div>
            <div class="search_options">
                <label><input type="checkbox" name="green" value="green" v-model="filter_rp_grades" /><span
                        class="toggle button" :class="{
                            green: filter_rp_grades.includes('green'),
                            fade_button: !filter_rp_grades.includes('green')
                        }">green</span></label>
                <label><input type="checkbox" name="yellow" value="yellow" v-model="filter_rp_grades" /><span
                        class="toggle button" :class="{
                            yellow: filter_rp_grades.includes('yellow'),
                            fade_button: !filter_rp_grades.includes('yellow')
                        }">yellow</span></label>
                <label><input type="checkbox" name="blue" value="blue" v-model="filter_rp_grades" /><span
                        class="toggle button" :class="{
                            blue: filter_rp_grades.includes('blue'),
                            fade_button: !filter_rp_grades.includes('blue')
                        }">blue</span></label>
                <label><input type="checkbox" name="purple" value="purple" v-model="filter_rp_grades" /><span
                        class="toggle button" :class="{
                            purple: filter_rp_grades.includes('purple'),
                            fade_button: !filter_rp_grades.includes('purple')
                        }">purple</span></label>
                <label><input type="checkbox" name="red" value="red" v-model="filter_rp_grades" /><span
                        class="toggle button" :class="{
                            red: filter_rp_grades.includes('red'),
                            fade_button: !filter_rp_grades.includes('red')
                        }">red</span></label>
                <label><input type="checkbox" name="brown" value="brown" v-model="filter_rp_grades" /><span
                        class="toggle button" :class="{
                            brown: filter_rp_grades.includes('brown'),
                            fade_button: !filter_rp_grades.includes('brown')
                        }">brown</span></label>
                <label><input type="checkbox" name="black" value="black" v-model="filter_rp_grades" /><span
                        class="toggle button" :class="{
                            black: filter_rp_grades.includes('black'),
                            fade_button: !filter_rp_grades.includes('black')
                        }">black</span></label>
                <label><input type="checkbox" name="turquoise" value="turquoise" v-model="filter_rp_grades" /><span
                        class="toggle button" :class="{
                            turquoise: filter_rp_grades.includes('turquoise'),
                            fade_button: !filter_rp_grades.includes('turquoise')
                        }">?</span></label>
            </div>
        </div>
        <label>Do you set problems?</label>
        <div>
            <select v-model="setter" name="setter">
                <option value="no">no</option>
                <option value="yes">yes</option>
            </select>
        </div>
        <div v-if="setter == 'yes'">
            <label for="setter_code">
                Setter code
            </label>
            <input v-model="setter_code" type="text" name="setter_code"
                placeholder="enter current code for 'grebrum'" />
            <p>status: <span v-if="setter_auth" class="green">setter code is linked successful</span><span v-else
                    class="orange">not linked</span></p>
            <button v-if="!setter_auth" :disabled="button_data.disabled" @click="link_setter_code">{{
                button_data.text
            }}</button>
            <p v-if="!setter_auth">* wait up to 15 seconds after clicking - status should be green</p>
            <p>
                <RouterLink :to="{ name: 'setter-stats' }">📊 Setter statistics</RouterLink>
            </p>
        </div>
    </div>
</template>


<style scoped>
.search_options .button {
    font-size: 0.65em;
    margin-right: 0.2em;
}

button {
    width: 100%;
}

.fade_button {
    background-color: hsl(207.9, 25%, 42.5%);
}

.labelblock {
    display: block;
}
</style>