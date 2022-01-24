import axios from 'axios';
const API_URL = 'http://localhost:8000';

export default class CategoriesService{

    getCategories() {
        const url = `${API_URL}/api/category/list/`;
        return axios.get(url).then(response => response.data);
    }
}