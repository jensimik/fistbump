<script setup>
import Layout from '../components/Layout.vue';
import ProblemsMethodsAPI from '../api/resources/ProblemsMethods.js'
import GradeDistribution from '../components/GradeDistribution.vue';
import HoldStats from '../components/HoldStats.vue';
import { ref } from 'vue'

const colors = ref({})
const grades = ref({})

const sections = { S1: "Section 1", S2: "Section 2", S3: "Section 3", S4: "Section 4", S5: "Section 5" }

for (const property in sections) {
    const data = await ProblemsMethodsAPI.index_section(property);
    colors.value[property] = data.colors;
    grades.value[property] = data.grades;
}


</script>

<template>
    <Layout>
        <template v-slot:content>
            <GradeDistribution></GradeDistribution>
            <HoldStats></HoldStats>
            <div v-for="(section_title, section_key) in sections" style="width:100%;">
                <h2>{{ section_title }}</h2>
                <div class="flex two">
                    <div class="third">Holds</div>
                    <div class="two-third right"><span class="label" :class="color" v-for="(c, color) in colors[section_key]">{{
                        c
                    }}</span></div>
                    <div class="third">Grades</div>
                    <div class="two-third right"><span class="label" :class="c[0]" v-for="c in grades[section_key]">{{
                        c[1]
                    }}</span>
                    </div>
                </div>
            </div>
        </template>
    </Layout>
</template>

<style scoped>
div.right {
    text-align: right;
}

span.grade {
    width: 5em;
}

span.label {
    margin-left: 0;
}
</style>