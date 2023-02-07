<script setup lang="ts">
import { useRegisterSW } from 'virtual:pwa-register/vue'

const intervalMS = 60 * 30 * 1000 // every 30 minutes

const {
    offlineReady,
    needRefresh,
    updateServiceWorker,
} = useRegisterSW({
    immediate: true,
    onRegisteredSW(swUrl, r) {
        const check = async () => {
            if (!(!r.installing && navigator))
                return

            if (('connection' in navigator) && !navigator.onLine)
                return

            const resp = await fetch(swUrl, {
                cache: 'no-store',
                headers: {
                    'cache': 'no-store',
                    'cache-control': 'no-cache',
                },
            });

            if (resp?.status === 200)
                await r.update();
        };
        // check periodic
        r && setInterval(async () => {
            await check();
        }, intervalMS);
        // check on visibilityChange on window 
        window.addEventListener('visibilitychange', check);
    },
})
const close = async () => {
    offlineReady.value = false
    needRefresh.value = false
}
const click_update = async () => {
    await updateServiceWorker();
    await new Promise(r => setTimeout(r, 1000));
    window.location.reload()
}
</script>

<template>
    <div v-if="needRefresh" class="pwa-toast" role="alert">
        <div class="message">
            New app version available, click on reload button to update.
        </div>
        <button class="button" v-if="needRefresh" @click="click_update">
            Reload
        </button>
    </div>
</template>

<style>
.pwa-toast {
    position: fixed;
    margin-left: auto;
    margin-right: auto;
    max-width: 800px;
    top: 0;
    right: 0;
    left: 0;
    padding: 12px;
    border: 1px solid #8885;
    border-radius: 4px;
    background-color: #fff;
    z-index: 10001;
    text-align: left;
    box-shadow: 3px 4px 5px 0px #8885;
}
</style>