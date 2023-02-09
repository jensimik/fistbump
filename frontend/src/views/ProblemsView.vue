<script setup>
import ProblemsMethodsAPI from '../api/resources/ProblemsMethods.js';
import Problem from '../components/Problem.vue'
import { filter_grades, filter_search_text, filter_sections, filter_gridview } from '../localStorage'
import { ref, watch } from 'vue';

const items = ref([]);

const toggle_gridview = async () => {
    filter_gridview = gridview ? false : true;
}

const refresh = async () => {
    items.value = await ProblemsMethodsAPI.search({ grades: filter_grades.value, sections: filter_sections.value, q: filter_search_text.value, limit: 100 });
}
watch([filter_sections, filter_grades, filter_search_text], async () => {
    await refresh();
});
await refresh();
</script>

<template>
    <div class="flex two">
        <div class="tight">
            <h2>Problems</h2>
        </div>
        <div class="tight right"><label><input type="checkbox" v-model="filter_gridview" /> <span class="checkable">grid
                    view</span></label></div>
    </div>
    <label for="free_text">Search</label>
    <input id="free_text" v-model="filter_search_text" type="search" />
    <div id="filter">
        <label>Filters</label>
        <div class="search_options">
            <label><input type="checkbox" name="S1" value="S1" v-model="filter_sections" /><span class="toggle button"
                    :class="{
                        fade_button: !filter_sections.includes('S1')
                    }">S1</span></label>
            <label><input type="checkbox" name="S2" value="S2" v-model="filter_sections" /><span class="toggle button"
                    :class="{
                        fade_button: !filter_sections.includes('S2')
                    }">S2</span></label>
            <label><input type="checkbox" name="S3" value="S3" v-model="filter_sections" /><span class="toggle button"
                    :class="{
                        fade_button: !filter_sections.includes('S3')
                    }">S3</span></label>
            <label><input type="checkbox" name="S4" value="S4" v-model="filter_sections" /><span class="toggle button"
                    :class="{
                        fade_button: !filter_sections.includes('S4')
                    }">S4</span></label>
            <label><input type="checkbox" name="S5" value="S5" v-model="filter_sections" /><span class="toggle button"
                    :class="{
                        fade_button: !filter_sections.includes('S5')
                    }">S5</span></label>
            <label><input type="checkbox" name="Ö" value="Ö" v-model="filter_sections" /><span class="toggle button"
                    :class="{
                        fade_button: !filter_sections.includes('Ö')
                    }">Stökt</span></label>
        </div>
        <div class="search_options">
            <label><input type="checkbox" name="green" value="green" v-model="filter_grades" /><span
                    class="toggle button" :class="{
                        green: filter_grades.includes('green'),
                        fade_button: !filter_grades.includes('green')
                    }">green</span></label>

            <label><input type="checkbox" name="yellow" value="yellow" v-model="filter_grades" /><span
                    class="toggle button" :class="{
                        yellow: filter_grades.includes('yellow'),
                        fade_button: !filter_grades.includes('yellow')
                    }">yellow</span></label>
            <label><input type="checkbox" name="blue" value="blue" v-model="filter_grades" /><span class="toggle button"
                    :class="{
                        blue: filter_grades.includes('blue'),
                        fade_button: !filter_grades.includes('blue')
                    }">blue</span></label>


            <label><input type="checkbox" name="purple" value="purple" v-model="filter_grades" /><span
                    class="toggle button" :class="{
                        purple: filter_grades.includes('purple'),
                        fade_button: !filter_grades.includes('purple')
                    }">purple</span></label>
            <label><input type="checkbox" name="red" value="red" v-model="filter_grades" /><span class="toggle button"
                    :class="{
                        red: filter_grades.includes('red'),
                        fade_button: !filter_grades.includes('red')
                    }">red</span></label>
            <label><input type="checkbox" name="brown" value="brown" v-model="filter_grades" /><span
                    class="toggle button" :class="{
                        brown: filter_grades.includes('brown'),
                        fade_button: !filter_grades.includes('brown')
                    }">brown</span></label>
            <label><input type="checkbox" name="black" value="black" v-model="filter_grades" /><span
                    class="toggle button" :class="{
                        black: filter_grades.includes('black'),
                        fade_button: !filter_grades.includes('black')
                    }">black</span></label>
            <label><input type="checkbox" name="turquoise" value="turquoise" v-model="filter_grades" /><span
                    class="toggle button" :class="{
                        black: filter_rp_grades.includes('turquoise'),
                        fade_button: !filter_rp_grades.includes('turquoise')
                    }">?</span></label>
        </div>
    </div>

    <div class="flex two" v-if="filter_gridview">
        <div v-for="item in items" :key="item.id">
            <Problem :data="item" slim="yes"></Problem>
        </div>
    </div>


    <table class="primary" v-else>
        <tbody>
            <tr v-for="item in items" :key="item.id">
                <td class="time">-{{ item.days_back }}d</td>
                <td class="section"><span v-if="item.color" class="label" :class="item.color"
                        :title="'holds color ' + item.color">{{ item.section }}</span><span v-else>{{
                            item.section
                        }}</span></td>
                <td class="name"><span><router-link :to="{ name: 'problem', params: { id: item.id } }">{{
                    item.name
                }}</router-link></span></td>
                <td class="tdgrade"><span class="label grade" :class="item.grade_class">{{
                    item.grade
                }}</span></td>
            </tr>
        </tbody>
    </table>

</template>

<style scoped>
/* .button:not(:last-child) {
    margin-right: 0.5em;
} */

.right {
    text-align: right;
    margin-top: auto;
    margin-bottom: auto;
}

.tight {
    padding-bottom: 0;
}

.button {
    margin-right: 0.5em;
}

.search_options .button {
    font-size: 0.65em;
}

.fade_button {
    background-color: hsl(207.9, 25%, 42.5%);
}



td.time {
    text-align: center;
    width: 2.5em;
}

td.section {
    width: 2.5em;
}

td.tdgrade {
    text-align: center;
    width: 5em;
}

td.name {
    width: calc(100% - 10em);
}

td.name span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: block;
    display: inline-block;
    white-space: nowrap;
    position: relative;
    width: 100%;
    margin-right: -1000px;
    vertical-align: middle;
}

td {
    padding-right: 0.1em;
    padding-left: 0;
}

tr td:first-child {
    padding-left: 0.3em;
}

tr td:last-child {
    padding-right: 0.3em;
}

span.grade {
    width: 5em;
}

td.section {
    text-align: center;
}

span.label {
    margin-left: 0;
}
</style>