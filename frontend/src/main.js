import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import * as Sentry from "@sentry/vue";
import Vue3TouchEvents from "vue3-touch-events";
// import { BrowserTracing } from "@sentry/tracing";


const app = createApp(App)

Sentry.init({
    app,
    dsn: "https://0d0b3deb62cc41dbbbd53509f51b3162@o4504589908377600.ingest.sentry.io/4504589910736897",
    // integrations: [
    //     new BrowserTracing({
    //         routingInstrumentation: Sentry.vueRouterInstrumentation(router),
    //         tracePropagationTargets: ["localhost", "my-site-url.com", /^\//],
    //     }),
    // ],
    // tracesSampleRate: 0.2,
});

app.use(Vue3TouchEvents)
app.use(router)

app.mount('#app')
