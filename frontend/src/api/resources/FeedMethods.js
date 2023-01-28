import { APISettings } from '../config.js';

export default {

    async index() {
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
    async index_section(section_id) {
        return fetch(APISettings.baseURL + '/section/' + section_id, {
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
    async get(item_id) {
        return fetch(APISettings.baseURL + '/feed/' + item_id, {
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
    async update(item_id, data) {
        return fetch(APISettings.baseURL + '/feed/' + item_id, {
            method: 'PUT',
            headers: APISettings,
            body: data
        })
            .then(function (response) {
                if (response.status != 200) {
                    throw response.status;
                } else {
                    return response.json();
                }
            });
    },
    async remove(item_id) {
        return fetch(APISettings.baseURL + '/feed/' + item_id, {
            method: 'DELETE',
            headers: APISettings,
        })
            .then(function (response) {
                if (response.status != 200) {
                    throw response.status;
                } else {
                    return response.json();
                }
            });
    },
    async store(data) {
        return fetch(APISettings.baseURL + '/feed', {
            method: 'POST',
            headers: APISettings,
            body: data
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