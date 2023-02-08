<script setup>
import { ref } from 'vue'
const props = defineProps(['data', 'slim', 'auth'])

const item = props.data;

const showHolds = ref(true);

const toggleShow = async () => {
    showHolds.value = showHolds.value ? false : true;
}
</script>

<template>
    <div v-if="props.slim" class="slim">
        <div class="imgw" v-if="item.section != 'Ö'">
            <router-link :to="{ name: 'problem', params: { id: item.id } }">
                <div v-if="item.image_width">
                    <svg :viewBox="'0 0 ' + item.image_width + ' ' + item.image_height"
                        xmlns="http://www.w3.org/2000/svg" class="problem">
                        <image :href="`https://fbs.gnerd.dk/webp/${item.image_hex}/800.webp`" :width="item.image_width"
                            :height="item.image_height" class="problem" />
                        <g v-show="showHolds">
                            <circle class="hold hand fat" :cx="a.cx" :cy="a.cy" r="80" :key="index"
                                v-for="(a, index) in item.annotations" />
                            <circle class="hold hand fat" :cx="a.cx" :cy="a.cy" r="115" :key="index"
                                v-for="(a, index) in item.annotations.slice(-item.holds_top)" v-if="item.holds_top" />
                            <g v-if="item.holds_start == 1">
                                <line :x1="a.cx + (Math.sin(-45) * 80)" :y1="a.cy + (Math.cos(-45) * 80)"
                                    :x2="a.cx + (Math.sin(-45) * 80) - 100" :y2="a.cy + (Math.cos(-45) * 80) + 100"
                                    class="hold hand fat" :key="index"
                                    v-for="(a, index) in item.annotations.slice(0, 1)" />
                                <line :x1="a.cx + (Math.sin(45) * 80)" :y1="a.cy + (Math.cos(45) * 80)"
                                    :x2="a.cx + (Math.sin(45) * 80) + 100" :y2="a.cy + (Math.cos(45) * 80) + 100"
                                    class="hold hand fat" :key="index"
                                    v-for="(a, index) in item.annotations.slice(0, 1)" />
                            </g>
                            <g v-if="item.holds_start == 2">
                                <line :x1="a.cx + (Math.sin(-45) * 80)" :y1="a.cy + (Math.cos(-45) * 80)"
                                    :x2="a.cx + (Math.sin(-45) * 80) - 100" :y2="a.cy + (Math.cos(-45) * 80) + 100"
                                    class="hold hand fat" :key="index"
                                    v-for="(a, index) in item.annotations.slice(0, 1)" />
                                <line :x1="a.cx + (Math.sin(45) * 80)" :y1="a.cy + (Math.cos(45) * 80)"
                                    :x2="a.cx + (Math.sin(45) * 80) + 100" :y2="a.cy + (Math.cos(45) * 80) + 100"
                                    class="hold hand fat" :key="index"
                                    v-for="(a, index) in item.annotations.slice(1, 2)" />
                            </g>
                        </g>
                    </svg>
                </div>
                <picture v-else>
                    <source type="image/webp" :srcset="`https://fbs.gnerd.dk/webp/${item.image_hex}/800.webp`" />
                    <img :src="`https://fbs.gnerd.dk/static/${item.image_hex}.jpg`" class="problem" />
                </picture>
            </router-link>
            <span class="label holds big left" :class="item.color" @click="toggleShow">holds</span>
            <span class="label grade big right" :class="item.grade_class">{{
                item.grade
            }}</span>
            <span class="label big setter white">{{ item.name }} ({{ item.setter }})</span>
        </div>
        <div class="imgw" v-else>
            <router-link :to="{ name: 'problem', params: { id: item.id } }">
                <svg width="100%" viewBox="0 0 2330 3000" xmlns="http://www.w3.org/2000/svg">
                    <image href="@/assets/stokt-wall.jpg" height="3000" width="2330" />
                    <path class="hold" :class="d.type" :d="d.path" v-for="d in item.paths" />
                </svg>
                <span class="label grade big right" :class="item.grade_class">{{
                    item.grade
                }}</span>
                <span class="label big setter white">{{ item.name }} ({{ item.setter }})</span>
            </router-link>
        </div>
    </div>
    <div v-else>
        <h2>{{ item.name }} (<router-link v-if="item.section != 'Ö'"
                :to="{ name: 'section', params: { id: item.section } }">{{
                    item.section
                }}</router-link><span v-else>{{ item.section }}</span>)</h2>
        <div v-if="item.section == 'Ö'">
            <div class="imgw">
                <svg width="100%" viewBox="0 0 2330 3000" xmlns="http://www.w3.org/2000/svg">
                    <image href="@/assets/stokt-wall.jpg" height="3000" width="2330" />
                    <path class="hold" :class="d.type" :d="d.path" v-for="d in item.paths" />
                </svg>
                <span class="label grade big right" :class="item.grade_class">{{
                    item.grade
                }}</span>
                <span class="label big left white">{{ item.setter }}</span>
            </div>
        </div>
        <div v-else>
            <p v-if="item.text">{{ item.text }}</p>
            <div class="imgw">
                <div v-if="item.image_width">
                    <svg :viewBox="'0 0 ' + item.image_width + ' ' + item.image_height"
                        xmlns="http://www.w3.org/2000/svg">
                        <image :href="`https://fbs.gnerd.dk/webp/${item.image_hex}/800.webp`" :width="item.image_width"
                            :height="item.image_height" class="problem" />
                        <g v-show="showHolds">
                            <circle class="hold hand fat" :cx="a.cx" :cy="a.cy" r="80" :key="index"
                                v-for="(a, index) in item.annotations" />
                            <circle class="hold hand fat" :cx="a.cx" :cy="a.cy" r="115" :key="index"
                                v-for="(a, index) in item.annotations.slice(-item.holds_top)" v-if="item.holds_top" />
                            <g v-if="item.holds_start == 1">
                                <line :x1="a.cx + (Math.sin(-45) * 80)" :y1="a.cy + (Math.cos(-45) * 80)"
                                    :x2="a.cx + (Math.sin(-45) * 80) - 100" :y2="a.cy + (Math.cos(-45) * 80) + 100"
                                    class="hold hand fat" :key="index"
                                    v-for="(a, index) in item.annotations.slice(0, 1)" />
                                <line :x1="a.cx + (Math.sin(45) * 80)" :y1="a.cy + (Math.cos(45) * 80)"
                                    :x2="a.cx + (Math.sin(45) * 80) + 100" :y2="a.cy + (Math.cos(45) * 80) + 100"
                                    class="hold hand fat" :key="index"
                                    v-for="(a, index) in item.annotations.slice(0, 1)" />
                            </g>
                            <g v-if="item.holds_start == 2">
                                <line :x1="a.cx + (Math.sin(-45) * 80)" :y1="a.cy + (Math.cos(-45) * 80)"
                                    :x2="a.cx + (Math.sin(-45) * 80) - 100" :y2="a.cy + (Math.cos(-45) * 80) + 100"
                                    class="hold hand fat" :key="index"
                                    v-for="(a, index) in item.annotations.slice(0, 1)" />
                                <line :x1="a.cx + (Math.sin(45) * 80)" :y1="a.cy + (Math.cos(45) * 80)"
                                    :x2="a.cx + (Math.sin(45) * 80) + 100" :y2="a.cy + (Math.cos(45) * 80) + 100"
                                    class="hold hand fat" :key="index"
                                    v-for="(a, index) in item.annotations.slice(1, 2)" />
                            </g>
                        </g>
                    </svg>
                </div>
                <picture v-else>
                    <source type="image/webp" :srcset="`https://fbs.gnerd.dk/webp/${item.image_hex}.webp`" />
                    <img :src="`https://fbs.gnerd.dk/static/${item.image_hex}.jpg`" class="problem" />
                </picture>
                <span class="label holds big left" :class="item.color" @click="toggleShow">holds</span>
                <span class="label grade big right" :class="item.grade_class">{{
                    item.grade
                }}</span>
                <span class="label big setter white">{{ item.setter }}</span>
            </div>
            <router-link v-if="props.auth" class="button"
                :to="{ name: 'problem_edit', params: { id: item.id } }">edit</router-link>
        </div>
    </div>
</template>

<style scoped>
svg {
    width: 100%;
}

.label {
    margin-left: 0;
}

.hold {
    stroke-width: 15px;
    fill: none;
}

.fat {
    stroke-width: 25px;
}

.foot {
    stroke: #39CCCC;
}

.hand {
    stroke: #fff;
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
}

.imgw {
    position: relative;
}

.big {
    position: absolute;
    border-radius: 0;
    font-size: 1.2em;
    opacity: 0.8;
}

.slim .big {
    font-size: 0.8em;
}

.left {
    top: 0;
    left: 0;
}

.right {
    top: 0;
    right: 0;
}

.setter {
    bottom: 0;
    left: 0;
    font-size: 0.5em !important;
}
</style>