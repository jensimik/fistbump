<script setup>
import StripMethodsAPI from '../api/resources/StripMethods.js'
import formatDistanceToNowStrict from 'date-fns/formatDistanceToNowStrict'
import format from 'date-fns/format'
import parseISO from 'date-fns/parseISO'
import { ref, onMounted, onBeforeUnmount } from 'vue'

const strip = ref({});


// refresh function
const refresh = async () => {
    strip.value = await StripMethodsAPI.index()
}

const visibilityChange = async () => {
    if (document.visibilityState === 'visible') {
        await refresh()
    }
}
onMounted(async () => {
    await refresh()
    document.addEventListener('visibilitychange', visibilityChange)
})

onBeforeUnmount(async () => {
    document.removeEventListener('visibilitychange', visibilityChange)
})
</script>

<template>
    <h2>{{ strip.section }} strip {{ format(parseISO(strip.datetime), 'd LLL') }}</h2>
    <p>{{ strip.setters }} | {{ formatDistanceToNowStrict(parseISO(strip.datetime)) }} days left to close it</p>
    <div>
        <svg width="276.38361mm" height="40.095062mm" viewBox="0 0 276.38361 40.095062" version="1.1" id="svg5"
            xml:space="preserve" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
            xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns="http://www.w3.org/2000/svg"
            xmlns:svg="http://www.w3.org/2000/svg">
            <defs id="defs2">
                <rect x="442.98984" y="323.13748" width="48.506527" height="43.333683" id="rect1764" />
                <rect x="24.720345" y="316.85254" width="50.724365" height="47.794785" id="rect1758" />
                <rect x="120.90091" y="360.72003" width="53.647594" height="50.845108" id="rect1752" />
                <rect x="270.44312" y="369.12112" width="92.100754" height="48.398495" id="rect1746" />
                <rect x="579.53638" y="383.96603" width="55.458725" height="37.487225" id="rect1740" />
                <rect x="738.49011" y="369.66129" width="57.174534" height="48.881462" id="rect1734" />
                <rect x="909.19391" y="369.64221" width="50.616333" height="43.43536" id="rect1522" />
            </defs>
            <g inkscape:label="Layer 1" inkscape:groupmode="layer" id="layer1"
                transform="translate(-2.5107788,-75.854509)">
                <path style="fill:#aaa;stroke-width:0.224601"
                    d="m 278.53838,101.04625 -9.24437,-18.629278 -23.73593,9.9368 -17.28409,0.780111 -7.43808,-3.135283 h -16.49015 l -17.03134,-9.745479 -6.55486,14.234838 -33.64786,1.364454 -10.23475,-15.049059 -10.48886,0.07564 v -4.734546 l 151.64754,0.629309 z"
                    id="path517" sodipodi:nodetypes="cccccccccccccc" />
                <path style="fill:#aaa;stroke-width:0.174517"
                    d="M 132.48143,115.02025 H 110.88908 V 98.668924 l 21.50488,-0.22883 0.0875,16.580156"
                    id="path519" />
                <g id="g554" transform="translate(-108.00552,2.2320417)" style="fill:#000000">
                    <path style="fill:#aaa;stroke-width:0.174517"
                        d="M 132.48143,113.64319 H 110.88908 V 97.291869 l 21.50488,-0.22883 0.0875,16.580151"
                        id="path519-3" />
                </g>
                <path style="fill:#aaa;stroke-width:0.264583"
                    d="m 112.27622,81.528719 h -7.12571 L 99.36654,91.464027 75.114231,91.73305 71.114215,89.727156 54.246552,89.991134 39.477259,86.584645 23.667187,87.35472 V 76.741813 l 89.096643,-0.07735 z"
                    id="path521" sodipodi:nodetypes="ccccccccccc" />
                <rect style="fill:none;stroke:#000;stroke-width:0.982157;stroke-dasharray:none;stroke-opacity:1"
                    id="rect569" width="275.40143" height="39.112911" x="3.0018573" y="76.345589" />
                <path style="fill:none;stroke:#929292;stroke-width:1.05833;stroke-dasharray:none;stroke-opacity:1"
                    d="M 221.59489,76.622435 V 115.14298" id="path1300" />
                <path style="fill:none;stroke:#929292;stroke-width:1.0392;stroke-dasharray:none;stroke-opacity:1"
                    d="M 186.54761,76.620752 V 114.53937" id="path1464" />
                <path style="fill:none;stroke:#929292;stroke-width:1.05833;stroke-dasharray:none;stroke-opacity:1"
                    d="M 54.470175,76.203769 V 114.66043" id="path1466" /><text xml:space="preserve"
                    transform="matrix(0.26458333,0,0,0.26458333,2.4548234,3.6334749)" id="text1520">
                    <tspan x="909.19336" y="398.75858" id="tspan1875">
                        <router-link :to="{ name: 'section', params: { id: 'S1' } }">
                            <tspan id="tspan1873">S1</tspan>
                        </router-link>
                    </tspan>
                </text><text xml:space="preserve" transform="matrix(0.26458333,0,0,0.26458333,4.2488621,3.9092222)"
                    id="text1732">
                    <router-link :to="{ name: 'section', params: { id: 'S2' } }">
                        <tspan x="738.49023" y="398.01568" id="tspan1877">S2</tspan>
                    </router-link>
                </text><text xml:space="preserve" transform="matrix(0.26458333,0,0,0.26458333,6.1690048,0)"
                    id="text1738">
                    <router-link :to="{ name: 'section', params: { id: 'S3' } }">
                        <tspan x="579.53711" y="412.32037" id="tspan1879">S3</tspan>
                    </router-link>
                </text><text xml:space="preserve" transform="matrix(0.26458333,0,0,0.26458333,5.2459239,3.5023268)"
                    id="text1744">
                    <router-link :to="{ name: 'section', params: { id: 'S4' } }">
                        <tspan x="270.44336" y="397.47466" id="tspan1881">S4</tspan>
                    </router-link>
                </text><text xml:space="preserve" transform="matrix(0.26458333,0,0,0.26458333,2.4699558,6.2715693)"
                    id="text1750">
                    <router-link :to="{ name: 'section', params: { id: 'S5' } }">
                        <tspan x="120.90039" y="389.07427" id="tspan1883">S5</tspan>
                    </router-link>
                </text><text xml:space="preserve" transform="matrix(0.26458333,0,0,0.26458333,0.51618546,2.6935802)"
                    id="text1756">
                    <tspan x="24.720703" y="345.20513" id="tspan1885">L</tspan>
                </text><text xml:space="preserve" transform="scale(0.26458333)" id="text1762">
                    <tspan x="442.99023" y="351.49029" id="tspan1887">Ö</tspan>
                </text>
            </g>
        </svg>
    </div>
</template>

<style scoped>
p {
    margin-top: 0;
    margin-bottom: 0;
}

svg {
    width: 100%;
}

svg text {
    font-size: 2em;
}
</style>