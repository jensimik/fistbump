import { APISettings } from '../config.js';

export default {

    index() {
        return fetch(APISettings.baseURL + '/feed', {
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
    store(data) {
        return fetch(APISettings.baseURL + '/feed', {
            method: 'POST',
            headers: { ...APISettings, ...{ 'Content-Type': 'application/json' } },
            body: JSON.stringify(data)
        })
            .then(function (response) {
                if (response.status != 201) {
                    throw response.status;
                } else {
                    return response.json();
                }
            });
    },
}