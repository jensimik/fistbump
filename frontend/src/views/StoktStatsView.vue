<script setup>
import Layout from '../components/Layout.vue';
import { ref } from 'vue'
import chroma from "chroma-js";

const colors = ref({})
const grades = ref({})

var scale = chroma.scale('OrRd').classes(6);

const data = [{"id": "707735", "count": 29, "path": "M792.96,146.93L761.69,139.11L734.40,160.44L688.25,177.12L630.80,171.21L623.68,194.93L668.44,238.52L724.59,245.39L770.42,213.32z"}, {"id": "708377", "count": 43, "path": "M1346.45,2032.38L1344.11,2062.74L1376.66,2072.62L1425.55,2062.25L1433.42,2045.42L1429.39,2023.93L1405.10,2020.73L1371.73,2024.47z"}, {"id": "708225", "count": 32, "path": "M799.21,189.29L769.61,208.12L764.80,250.19L785.17,306.76L822.54,320.60L853.91,289.24L855.06,238.57L832.66,197.32z"}]

</script>

<template>
    <Layout>
        <template v-slot:content>
            <div class="imgw">
                <svg width="100%" viewBox="0 0 2330 3000" xmlns="http://www.w3.org/2000/svg">
                    <image href="@/assets/stokt-wall.jpg" height="3000" width="2330" />
                    <g>
                        <path class="hold stokt-hold hand" :id="d.id" :d="d.path" :fill="scale(d.count/25).hex()" v-for="d in data" />
                    </g>
                </svg>
            </div>
        </template>
    </Layout>
</template>

<style scoped>
svg {
    width: 100%;
}

.label {
    margin-left: 0;
}

.hold {
    /* stroke-width: 15px; */
    /* fill: none; */
    opacity: 0.5;
}

.stokt-hold {
    stroke-width: 10px;
    stroke: #000;
}
.lumo-hold {
    stroke: #000;
    stroke-width: 4px;
}
.text {
    font-size: 15px;
}
.foot {
    stroke: #39CCCC;
}

.hand {
    /* stroke: #ff0000; */
}

wrapper {
    position: relative;
    display: inline-block;
}

.problem {
    width: 100%;
    display: block;
    aspect-ratio: 3/4;
    object-fit: cover;
    object-position: left;
}</style>