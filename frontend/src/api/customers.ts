import { api, unpackPage } from './clients'
import type { Customer, Address, Paginated, UUID } from '../types'


export async function listCustomers(params: {
    page?: number
    page_size?: number
    search?: string
    city?: string
    state?: string
    pincode?: string
    ordering?: string
}) {
    const { data } = await api.get<Paginated<Customer>>('/customers/', { params })
    return unpackPage<Customer>(data)
}


export async function createCustomer(payload: Partial<Customer>) {
    const { data } = await api.post<Customer>('/customers/', payload)
    return data
}


export async function getCustomer(id: UUID) {
    const { data } = await api.get<Customer>(`/customers/${id}`)
    return data
}


export async function updateCustomer(id: UUID, payload: Partial<Customer>) {
    const { data } = await api.patch<Customer>(`/customers/${id}`, payload)
    return data
}


export async function deleteCustomer(id: UUID) {
    await api.delete(`/customers/${id}`)
}


// Addresses (nested)
export async function listAddresses(customerId: UUID) {
    const { data } = await api.get<{ count: number; data: Address[]; primary_address?: Address | null }>(
        `/customers/${customerId}/addresses`
    )
    return data
}


export async function createAddress(customerId: UUID, payload: Partial<Address>) {
    const { data } = await api.post<Address>(`/customers/${customerId}/addresses/`, payload)
    return data
}


export async function updateAddress(customerId: UUID, addressId: UUID, payload: Partial<Address>) {
    const { data } = await api.patch<Address>(`/customers/${customerId}/addresses/${addressId}`, payload)
    return data
}


export async function deleteAddress(customerId: UUID, addressId: UUID) {
    await api.delete(`/customers/${customerId}/addresses/${addressId}`)
}