import axios from 'axios'

var BaseUrl = "http://localhost:8008";

function get(url) {
    return axios.get(this.BaseUrl + url);
}

function post(url, data) {
    return axios.post(this.BaseUrl + url, data);
}

function opendownload(url) {
    window.open(this.BaseUrl + url, '_blank')
}

function getBaseUrl() {
    return this.BaseUrl;
} 

export default {
    BaseUrl,
    getBaseUrl,
    get,
    post,
    opendownload
}