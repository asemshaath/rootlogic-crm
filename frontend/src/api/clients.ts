import axios from 'axios'
// import env from "react-dotenv";

const baseURL = `${import.meta.env.VITE_API_BASE_URL}/api/` 
export const api = axios.create({
    baseURL,
    headers: { 'Content-Type': 'application/json' }
})


api.interceptors.response.use(
    (r) => r,
    (error) => {
        const e = error
        let message = 'Request failed'
        if (e.response?.data) {
            const d = e.response.data
            if (typeof d === 'string') message = d
            else if (d.detail) message = d.detail
            else message = JSON.stringify(d)
        } else if (e.message) message = e.message
            return Promise.reject(new Error(message))
    }
)


// Helpers to map `results`|`data`
export function unpackPage<T>(payload: any): { items: T[]; count: number } {
    const items: T[] = payload?.results ?? payload?.data ?? []
    const count: number = payload?.count ?? items.length
    return { items, count }
}