<script setup>
import Layout from '../components/Layout.vue';
import ProblemsMethodsAPI from '../api/resources/ProblemsMethods.js'
import Problem from '../components/Problem.vue'
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps(['id'])

const items = ref([])
const colors = ref({})
const grades = ref({})

// refresh function
const refresh = async () => {
    const data = await ProblemsMethodsAPI.index_section(props.id)
    items.value = data.data;
    colors.value = data.colors;
    grades.value = data.grades
}

const visibilityChange = async () => {
    if (document.visibilityState === 'visible') {
        await refresh()
    }
}
onMounted(async () => {
    await refresh();
    document.addEventListener('visibilitychange', visibilityChange)
})

onBeforeUnmount(async () => {
    document.removeEventListener('visibilitychange', visibilityChange)
})
</script>

<template>
    <Layout>
        <template v-slot:content>
            <h2>Problems on section {{ props.id }}</h2>
            <div class="flex two">
                <div class="third">Holds colors</div>
                <div class="two-third right"><span class="label" :class="color" v-for="(c, color) in colors">{{ c }}</span>
                </div>
                <div class="third">Grades</div>
                <div class="two-third right"><span class="label" :class="c[0]" v-for="c in grades">{{ c[1] }}</span></div>
            </div>
            <div class="flex two">
                <div v-for="item in items" :key="item.id">
                    <Problem :data="item" slim="yes"></Problem>
                </div>
            </div>
        </template>
    </Layout>
</template>

<style scoped>
div.right {
    text-align: right;
}

h2 {
    padding: 0;
}

span.grade {
    width: 5em;
}

span.label {
    margin-left: 0;
}
</style>
