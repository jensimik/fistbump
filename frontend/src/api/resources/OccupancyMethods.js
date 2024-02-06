import { APISettings } from '../config.js';

export default {

    index() {
        return fetch('https://lockoff-api.gnerd.dk/occupancy', {
            method: 'GET',
            headers: APISettings.headers
        })
            .then(function (response) {
                if (response.status != 200) {
                    throw response.status;
                } else {
                    return response.json();
                }
            });
    },
}