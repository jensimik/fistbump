import { APISettings } from '../config.js';

export default {

    get(setter_code) {
        return fetch(APISettings.baseURL + '/setter-code/' + setter_code, {
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