import "../node_modules/picnic/picnic.min.css";
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import * as Sentry from "@sentry/vue";
import { BrowserTracing } from "@sentry/tracing";
import VueMixpanel from 'vue-mixpanel'

const app = createApp(App)

Sentry.init({
    app,
    dsn: "https://0d0b3deb62cc41dbbbd53509f51b3162@o4504589908377600.ingest.sentry.io/4504589910736897",
    environment: import.meta.env.PROD ? "production" : "development",
    integrations: [
        new BrowserTracing({
            routingInstrumentation: Sentry.vueRouterInstrumentation(router),
            tracePropagationTargets: ["localhost", "fb-api.gnerd.dk", /^\//],
        }),
    ],
    tracesSampleRate: 0.2,
});

app.use(router)
app.use(VueMixpanel, {
    token: "34cedfac2ebbc776f77cc53866e9e63e",
    config: {
      debug: true
    }
  })


app.mount('#app')
