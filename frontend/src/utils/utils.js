import axios from 'axios';
import Cookies from 'universal-cookie';
import {store} from '../redux/store';
import {setCurrentUserAsync} from '../redux/user/user.actions';


let access_token = '';
const backend_host = 'http://localhost:8000/api';

export class SmartRequest {
    static async refresh_token(cookies) {
        await axios.post(`${backend_host}/refresh_token/`,
            {},
            {
                withCredentials: true,
                headers: {'X-CSRFToken': cookies.get('csrftoken')}
            })
            .then(resp => {
                access_token = resp.data['access']
                console.log('success refresh:', resp)
            })
            .catch(error => {
                console.error('error in refresh:', error.response)
                if (error.response === undefined) {
                    throw Error('Back end does not send the response, maybe you forget to run the back end server?')
                }
                if (error.response.status === 401) {
                    console.log('set current user to null because refresh token is missing, expired or invalid')
                    store.dispatch(setCurrentUserAsync(null))
                    throw error
                }
            })
    }

    static async prepareData(url, config, shouldRefresh) {
        if (!url) {
            throw new TypeError('Url cannot be empty')
        }

        const cookies = new Cookies()

        if (access_token === '' && shouldRefresh) {
            await this.refresh_token(cookies)
        }

        url = url.replace(backend_host, '')
        if (!url.startsWith('/')) {
            url = `/${url}`
        }
        url = `${backend_host}${url}`

        config = {
            ...config,
            withCredentials: true,
            headers: {
                ...config.headers,
                'X-CSRFToken': cookies.get('csrftoken'),
                'AUTHORIZATION': access_token && shouldRefresh ? 'Bearer ' + access_token : ''
            }
        }

        return [url, config]
    }

    static async post(url, data = {}, config = {}, shouldTryAgain = true, shouldRefresh = true) {
        [url, config] = await this.prepareData(url, config, shouldRefresh)


        return axios.post(url, data, config)
            .catch((error) => {
                if (error.response.status === 403) {
                    access_token = ''
                    if (shouldTryAgain) {
                        return this.post(url, data, config, false)
                    }
                }
                throw error
            })
    }

    static async get(url, config = {}, shouldTryAgain = true, shouldRefresh = true) {
        [url, config] = await this.prepareData(url, config, shouldRefresh)

        return axios.get(url, config)
            .catch((error) => {
                if (error.response.status === 403) {
                    access_token = ''
                    if (shouldTryAgain) {
                        return this.get(url, config, false)
                    }
                }
                throw error
            })
    }

    static async patch(url, data = {}, config = {}, shouldTryAgain = true, shouldRefresh = true) {
        [url, config] = await this.prepareData(url, config, shouldRefresh)


        return axios.patch(url, data, config)
            .catch((error) => {
                if (error.response.status === 403) {
                    access_token = ''
                    if (shouldTryAgain) {
                        return this.patch(url, data, config, false)
                    }
                }
                throw error
            })
    }

    static setAccessToken(token) {
        access_token = token
    }
}


