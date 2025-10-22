import * as React from 'react'
import { Stack, TextField, Button } from '@mui/material'
import type { Customer } from '../types'
import { useState } from 'react'

export default function CustomerForm({ initial, onSubmit, submitting }: {
    initial?: Partial<Customer>
    submitting?: boolean
    onSubmit: (values: Partial<Customer>) => void
}) {
    const [values, setValues] = useState<Partial<Customer>>({
        first_name: initial?.first_name ?? '',
        last_name: initial?.last_name ?? '',
        email: initial?.email ?? '',
        phone_number: initial?.phone_number ?? ''
    })


    const handleChange = (field: keyof Customer) => (e: React.ChangeEvent<HTMLInputElement>) => {
        setValues((v) => ({ ...v, [field]: e.target.value }))
    }


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        console.log("Form submit triggered") 
        try {
            await onSubmit(values)     
        } catch (err) {
            console.error('Form submit error:', err)
        }
    }


    return (
    <form onSubmit={handleSubmit} noValidate>
        <Stack spacing={2}>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                <TextField required label="First name" value={values.first_name} onChange={handleChange('first_name')} />
                <TextField required label="Last name" value={values.last_name} onChange={handleChange('last_name')} />
            </Stack>
            <TextField required type="email" label="Email" value={values.email} onChange={handleChange('email')} />
            <TextField label="Phone" value={values.phone_number} onChange={handleChange('phone_number')} />
            <Stack direction="row" spacing={2}>
                <Button type="submit" variant="contained" disabled={submitting}>Save</Button>
            </Stack>
        </Stack>
    </form>
    )
}