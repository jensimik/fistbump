import { APISettings } from '../config.js';

export default {

    async index() {
        return fetch(APISettings.baseURL + '/problems', {
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
    async search(params) {
        return fetch(APISettings.baseURL + '/problems?' + new URLSearchParams(params), {
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
        return fetch(APISettings.baseURL + '/sections/' + section_id, {
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
        return fetch(APISettings.baseURL + '/problems/' + item_id, {
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
    async update(item_id, data, auth) {
        return fetch(APISettings.baseURL + '/problems/' + item_id, {
            method: 'PUT',
            headers: { ...APISettings.headers, access_token: auth },
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
    async remove(item_id, auth) {
        return fetch(APISettings.baseURL + '/problems/' + item_id, {
            method: 'DELETE',
            headers: { ...APISettings.headers, access_token: auth },
        })
            .then(function (response) {
                if (response.status != 200) {
                    throw response.status;
                } else {
                    return response.json();
                }
            });
    },
    async store(data, auth) {
        return fetch(APISettings.baseURL + '/problems', {
            method: 'POST',
            headers: { ...APISettings, access_token: auth },
            body: data
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