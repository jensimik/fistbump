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

var bluetooth_server;

const write_lumo = async () => {
    navigator.bluetooth.requestDevice({
        filters: [{ name: "Lumo Wall"}]
    }).then(function(device) {
        // connect to it
        return device.gatt.connect();
    }).then(function(server) {
        bluetooth_server = server;
        // get the service
        return server.getPrimaryService("1d2f4e96-44e3-437d-b808-2de657f56879");
    }).then(function(service) {
        // get the Characteristic
        return service.getCharacteristic("5ccf53e6-617d-43d4-ad94-4ddb5b5951c1");
    }).then(function(characteristic) {
        // write to the characteristic
        var data = new Uint8Array([10, 10, 10, 11, 255, 10, 12, 255, 10, 13, 10, 14, 255, 0]);
        return characteristic.writeValueWithoutResponse(data);
    }).then(function(done) {
        // disconnect again
        return bluetooth_server.disconnect();
    }).catch(function(error) {     console.error('Connection failed!', error);
  });
}

</script>

<template>
    <div v-if="props.slim" class="slim">
        <div class="imgw" v-if="item.section.startsWith('S')">
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
        <div v-else-if="item.section == 'L'" class="imgw">
            <router-link :to="{ name: 'problem', params: { id: item.id } }">
                <svg viewBox="0 0 840 960" xmlns="http://www.w3.org/2000/svg" class="problem">
                    <g>
                        <rect x="0" width="840" height="960" fill="#dfdfdf"></rect>
                    </g>
                    <g v-for="row in 23" :key="row">
                        <g v-for="column in 20" :key="column">
                            <circle r="15" :cx="column * 40" :cy="960 - (row * 40)" fill="#d0d0d0" class="hold hand fat" :title="row + ',' + column"></circle>
                            <text v-if="row == 1" :x="column * 40" :y="960 - (row * 40)" stroke="#d0d0d0" stroke-width="1px" text-anchor="middle" dominant-baseline="central" class="text">{{ column }}</text>
                            <text v-if="column == 1" :x="column * 40" :y="960 - (row * 40)" stroke="#d0d0d0" stroke-width="1px" text-anchor="middle" dominant-baseline="central" class="text">{{ row }}</text>
                        </g>
                    </g>
                    <g>
                        <circle v-for="hold in item.lumo_hands" :key="hold" r="15" :cx="(1+hold[0]) * 40" :cy="960 - ((1+hold[1]) * 40)" fill="#fff" class="lumo-hold"></circle>
                        <circle v-for="hold in item.lumo_feet" :key="hold" r="7" :cx="(1+hold[0]) * 40" :cy="960 - ((1+hold[1]) * 40)" fill="#fff" class="lumo-hold" :data="hold"></circle>
                        <circle v-for="hold in item.lumo_sf" :key="hold" r="15" :cx="(1+hold[0]) * 40" :cy="960 - ((1+hold[1]) * 40)" fill="#FFDC00" class="lumo-hold"></circle>
                    </g>
                </svg>
            </router-link>
            <span class="label hgs info-right" :class="item.grade_class">{{ item.grade }}</span>
            <span class="label hgs info-left rainbow" @click="toggleShow">holds</span>
            <span class="label info-right-bottom hgs white">{{ item.setter }}</span>
            <span class="label info-left-bottom hgs white">{{ item.name }}</span>
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
        <div v-else-if="item.section == 'L'">
            <div class="imgw">
                <svg viewBox="0 0 840 960" xmlns="http://www.w3.org/2000/svg" class="problem">
                    <g>
                        <rect x="0" width="840" height="960" fill="#dfdfdf"></rect>
                    </g>
                    <g v-for="row in 23" :key="row">
                        <g v-for="column in 20" :key="column">
                            <circle r="15" :cx="column * 40" :cy="960 - (row * 40)" fill="#d0d0d0" class="hold hand fat" :title="row + ',' + column"></circle>
                            <text v-if="row == 1" :x="column * 40" :y="960 - (row * 40)" stroke="#d0d0d0" stroke-width="1px" text-anchor="middle" dominant-baseline="central" class="text">{{ column }}</text>
                            <text v-if="column == 1" :x="column * 40" :y="960 - (row * 40)" stroke="#d0d0d0" stroke-width="1px" text-anchor="middle" dominant-baseline="central" class="text">{{ row }}</text>
                        </g>
                    </g>
                    <g>
                        <circle v-for="hold in item.lumo_hands" :key="hold" r="15" :cx="(1+hold[0]) * 40" :cy="960 - ((1+hold[1]) * 40)" fill="#fff" class="lumo-hold"></circle>
                        <circle v-for="hold in item.lumo_feet" :key="hold" r="7" :cx="(1+hold[0]) * 40" :cy="960 - ((1+hold[1]) * 40)" fill="#fff" class="lumo-hold" :data="hold"></circle>
                        <circle v-for="hold in item.lumo_sf" :key="hold" r="15" :cx="(1+hold[0]) * 40" :cy="960 - ((1+hold[1]) * 40)" fill="#FFDC00" class="lumo-hold"></circle>
                    </g>
                </svg>
                <span class="label hgs info-right" :class="item.grade_class">{{ item.grade }}</span>
                <span class="label hgs info-left rainbow" @click="toggleShow">holds</span>
                <span class="label info-right-bottom hgs white">{{ item.setter }} </span>
                <span class="label info-left-bottom hgs white">{{ item.name }}test</span>
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