import axios from 'axios'

var BaseUrl = "http://localhost:8008";

function get(url) {
    return axios.get(this.BaseUrl + url);
}

function post(url, data) {
    return axios.post(this.BaseUrl + url, data);
}

export default {
    BaseUrl,
    get,
    post
}