export type UUID = string


export interface Customer {
    id: string
    // uuid: UUID
    first_name: string
    last_name: string
    email: string
    phone_number?: string
    created_at?: string
    updated_at?: string
    num_of_addresses?: number
}


export interface Address {
    id: UUID
    customer: UUID
    address_line1: string
    address_line2?: string
    city: string
    state: string
    pincode: string
    is_primary?: boolean
    country?: string
}


export interface Paginated<T> {
    count: number
    next?: string | null
    previous?: string | null
    results?: T[]
    data?: T[] // some APIs return `data` instead of `results`
}