import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import * as Sentry from "@sentry/vue";
import { BrowserTracing } from "@sentry/tracing";


const app = createApp(App)

Sentry.init({
    app,
    dsn: "https://0d0b3deb62cc41dbbbd53509f51b3162@o4504589908377600.ingest.sentry.io/4504589910736897",
    integrations: [
        new BrowserTracing({
            routingInstrumentation: Sentry.vueRouterInstrumentation(router),
            tracePropagationTargets: ["localhost", "my-site-url.com", /^\//],
        }),
    ],
    tracesSampleRate: 1.0,
});

app.use(router)

app.mount('#app')
