<script setup>
import { ref } from 'vue'
const props = defineProps(['data', 'slim', 'auth'])

const item = props.data;

const showHolds = ref(true);

const radius = item.image_width / 38;
const stroke_width = item.image_width / 121;

const toggleShow = async () => {
    showHolds.value = showHolds.value ? false : true;
}
</script>

<template>
    <div v-if="props.slim" class="slim">
        <div class="imgw" v-if="item.section != 'Ö'">
            <router-link :to="{ name: 'problem', params: { id: item.id } }">
                <div v-if="item.image_width">
                    <svg :viewBox="'0 0 ' + item.image_width + ' ' + item.image_height" xmlns="http://www.w3.org/2000/svg"
                        class="problem">
                        <image :href="`https://ik.imagekit.io/gnerd/tr:w-400/${item.image_hex}.jpg`"
                            :width="item.image_width" :height="item.image_height" class="problem" />
                        <g v-show="showHolds">
                            <circle class="hold hand fat" :cx="a.cx" :cy="a.cy" :r="radius" :stroke-width="stroke_width" :key="index"
                                v-for="(a, index) in item.annotations" />
                            <circle class="hold hand fat" :cx="a.cx" :cy="a.cy" :r="radius + 35" :stroke-width="stroke_width" :key="index"
                                v-for="(a, index) in item.annotations.slice(-item.holds_top)" v-if="item.holds_top" />
                            <g v-if="item.holds_start == 1">
                                <line :x1="a.cx + (Math.sin(-45) * radius)" :y1="a.cy + (Math.cos(-45) * radius)"
                                    :x2="a.cx + (Math.sin(-45) * radius) - radius" :y2="a.cy + (Math.cos(-45) * 80) + radius"
                                    class="hold hand fat" :stroke-width="stroke_width" :key="index" v-for="(a, index) in item.annotations.slice(0, 1)" />
                                <line :x1="a.cx + (Math.sin(45) * radius)" :y1="a.cy + (Math.cos(45) * radius)"
                                    :x2="a.cx + (Math.sin(45) * radius) + radius" :y2="a.cy + (Math.cos(45) * radius) + radius"
                                    class="hold hand fat" :stroke-width="stroke_width" :key="index" v-for="(a, index) in item.annotations.slice(0, 1)" />
                            </g>
                            <g v-if="item.holds_start == 2">
                                <line :x1="a.cx + (Math.sin(-45) * radius)" :y1="a.cy + (Math.cos(-45) * radius)"
                                    :x2="a.cx + (Math.sin(-45) * radius) - radius" :y2="a.cy + (Math.cos(-45) * radius) + radius"
                                    class="hold hand fat" :stroke-width="stroke_width" :key="index" v-for="(a, index) in item.annotations.slice(0, 1)" />
                                <line :x1="a.cx + (Math.sin(45) * radius)" :y1="a.cy + (Math.cos(45) * radius)"
                                    :x2="a.cx + (Math.sin(45) * radius) + radius" :y2="a.cy + (Math.cos(45) * radius) + radius"
                                    class="hold hand fat" :stroke-width="stroke_width" :key="index" v-for="(a, index) in item.annotations.slice(1, 2)" />
                            </g>
                        </g>
                    </svg>
                </div>
                <img v-else :src="`https://ik.imagekit.io/gnerd/tr:w-400/${item.image_hex}.jpg`" class="problem" />
            </router-link>
            <span class="label info-left hgs" :class="item.color" @click="toggleShow">holds</span>
            <span class="label info-right hgs" :class="item.grade_class">{{ item.grade }}</span>
            <span class="label info-left-bottom hgs white">{{ item.name }} ({{ item.setter }})</span>
        </div>
        <div class="imgw" v-else>
            <router-link :to="{ name: 'problem', params: { id: item.id } }">
                <svg width="100%" viewBox="0 0 2330 3000" xmlns="http://www.w3.org/2000/svg">
                    <image href="@/assets/stokt-wall.jpg" height="3000" width="2330" />
                    <path class="hold stokt-hold" :class="d.type" :d="d.path" v-for="d in item.paths" />
                </svg>
                <span class="label hgs info-left rainbow">holds</span>
                <span class="label hgs info-right" :class="item.grade_class">{{
                    item.grade
                }}</span>
                <span class="label hgs info-left-bottom white">{{ item.name }} ({{ item.setter }})</span>
            </router-link>
        </div>
    </div>
    <div v-else>
        <div v-if="item.section == 'Ö'">
            <div class="imgw">
                <svg width="100%" viewBox="0 0 2330 3000" xmlns="http://www.w3.org/2000/svg">
                    <image href="@/assets/stokt-wall.jpg" height="3000" width="2330" />
                    <g v-show="showHolds">
                        <path class="hold stokt-hold" :class="d.type" :d="d.path" v-for="d in item.paths" />
                    </g>
                </svg>
                <span class="label hgs info-right" :class="item.grade_class">{{ item.grade }}</span>
                <span class="label hgs info-left rainbow" @click="toggleShow">holds</span>
                <span class="label info-right-bottom hgs white">{{ item.setter }}</span>
                <span class="label info-left-bottom hgs white">{{ item.name }}</span>
            </div>
        </div>
        <div v-else>
            <p v-if="item.text">{{ item.text }}</p>
            <div class="imgw">
                <div v-if="item.image_width">
                    <svg :viewBox="'0 0 ' + item.image_width + ' ' + item.image_height" xmlns="http://www.w3.org/2000/svg">
                        <image :href="`https://ik.imagekit.io/gnerd/tr:w-800/${item.image_hex}.jpg`"
                            :width="item.image_width" :height="item.image_height" class="problem" />
                        <g v-show="showHolds">
                            <circle class="hold hand fat" :cx="a.cx" :cy="a.cy" :r="radius" :stroke-width="stroke_width" :key="index"
                                v-for="(a, index) in item.annotations" />
                            <circle class="hold hand fat" :cx="a.cx" :cy="a.cy" :r="radius + 35" :stroke-width="stroke_width" :key="index"
                                v-for="(a, index) in item.annotations.slice(-item.holds_top)" v-if="item.holds_top" />
                            <g v-if="item.holds_start == 1">
                                <line :x1="a.cx + (Math.sin(-45) * radius)" :y1="a.cy + (Math.cos(-45) * radius)"
                                    :x2="a.cx + (Math.sin(-45) * radius) - radius" :y2="a.cy + (Math.cos(-45) * radius) + radius"
                                    class="hold hand fat" :stroke-width="stroke_width" :key="index" v-for="(a, index) in item.annotations.slice(0, 1)" />
                                <line :x1="a.cx + (Math.sin(45) * radius)" :y1="a.cy + (Math.cos(45) * radius)"
                                    :x2="a.cx + (Math.sin(45) * radius) + radius" :y2="a.cy + (Math.cos(45) * radius) + radius"
                                    class="hold hand fat" :stroke-width="stroke_width" :key="index" v-for="(a, index) in item.annotations.slice(0, 1)" />
                            </g>
                            <g v-if="item.holds_start == 2">
                                <line :x1="a.cx + (Math.sin(-45) * radius)" :y1="a.cy + (Math.cos(-45) * radius)"
                                    :x2="a.cx + (Math.sin(-45) * radius) - radius" :y2="a.cy + (Math.cos(-45) * radius) + radius"
                                    class="hold hand fat" :stroke-width="stroke_width" :key="index" v-for="(a, index) in item.annotations.slice(0, 1)" />
                                <line :x1="a.cx + (Math.sin(45) * radius)" :y1="a.cy + (Math.cos(45) * radius)"
                                    :x2="a.cx + (Math.sin(45) * radius) + radius" :y2="a.cy + (Math.cos(45) * radius) + radius"
                                    class="hold hand fat" :stroke-width="stroke_width" :key="index" v-for="(a, index) in item.annotations.slice(1, 2)" />
                            </g>
                        </g>
                    </svg>
                </div>
                <img v-else :src="`https://ik.imagekit.io/gnerd/tr:w-800/${item.image_hex}.jpg`" class="problem" />
                <span class="label info-left hgs" :class="item.color" @click="toggleShow">holds</span>
                <span class="label info-right hgs" :class="item.grade_class">{{ item.grade }}</span>
                <span class="label info-right-bottom hgs white">{{ item.setter }}</span>
                <span class="label info-left-bottom hgs white">{{ item.name }}</span>
            </div>
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
    /* stroke-width: 15px; */
    fill: none;
}

.stokt-hold {
    stroke-width: 15px;
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

.info-left {
    position: absolute;
    top: 0;
    left: 0;
}
.info-left-bottom {
    position: absolute;
    bottom: 0.3em;
    left: 0;
}
.slim .info-left-bottom {
    bottom: 0em;
    font-size: 0.5em !important;
}
.info-right {
    position: absolute;
    top: 0;
    right: 0;
}
.info-right-bottom {
    position: absolute;
    bottom: 0.3em;
    right: 0;
}

.hgs {
    border-radius: 0;
    font-size: 1.2em;
    opacity: 0.7;
}
.white {
    opacity: 0.5;
}
.slim .hgs {
    font-size: 0.8em;
}
</style>