<script setup lang="ts">
import { useRegisterSW } from 'virtual:pwa-register/vue'
import { pwaInfo } from 'virtual:pwa-info'
// eslint-disable-next-line no-console
console.log(pwaInfo)
// replaced dyanmicaly
const reloadSW: any = '__RELOAD_SW__'
const {
    offlineReady,
    needRefresh,
    updateServiceWorker,
} = useRegisterSW({
    immediate: true,
    onRegisteredSW(swUrl, r) {
        // eslint-disable-next-line no-console
        console.log(`Service Worker at: ${swUrl}`)
        if (reloadSW === 'true') {
            r && setInterval(async () => {
                // eslint-disable-next-line no-console
                console.log('Checking for sw update')
                await r.update()
            }, 20000 /* 20s for testing purposes */)
        }
        else {
            // eslint-disable-next-line no-console
            console.log(`SW Registered: ${r}`)
        }
    },
})
const close = async () => {
    offlineReady.value = false
    needRefresh.value = false
}
const click_update = async () => {
    updateServiceWorker()
    window.location.reload()
}
</script>

<template>
    <div v-if="needRefresh" class="pwa-toast" role="alert">
        <div class="message">
            New content available, click on reload button to update.
        </div>
        <button class="button" v-if="needRefresh" @click="click_update">
            Reload
        </button>
        <button class="button" @click="close">
            Close
        </button>
    </div>
</template>

<style>
.pwa-toast {
    position: absolute;
    right: 0;
    bottom: 0;
    margin: 16px;
    padding: 12px;
    border: 1px solid #8885;
    border-radius: 4px;
    background-color: #fff;
    z-index: 1;
    text-align: left;
    box-shadow: 3px 4px 5px 0px #8885;
}
</style>