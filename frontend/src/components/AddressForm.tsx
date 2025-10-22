import * as React from 'react'
import { Stack, TextField, Checkbox, FormControlLabel, Button, Input, Select, InputLabel, Menu, MenuItem } from '@mui/material'
import type { Address } from '../types'
import { useState } from 'react'
import { FormControl } from '@mui/material'

export default function AddressForm({ initial, onSubmit, submitting }: {
    initial?: Partial<Address>
    submitting?: boolean
    onSubmit: (values: Partial<Address>) => void
}) {
const [values, setValues] = useState<Partial<Address>>({
    address_line1: initial?.address_line1 ?? '',
    address_line2: initial?.address_line2 ?? '',
    city: initial?.city ?? '',
    state: initial?.state ?? '',
    pincode: initial?.pincode ?? '',
    is_primary: initial?.is_primary ?? false
})

const change = (k: keyof Address) => (e: any) => {
  const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value
  setValues(v => ({ ...v, [k]: value }))
}

const submit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(values); 
}

return (
    <form onSubmit={submit} noValidate>
        <Stack spacing={2}>
            <TextField required label="Address line 1" value={values.address_line1} onChange={change('address_line1')} />
            <TextField label="Address line 2" value={values.address_line2} onChange={change('address_line2')} />
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                <TextField required label="City" value={values.city} onChange={change('city')} />
                <TextField required label="State" value={values.state} onChange={change('state')} />
                <TextField required label="Pincode" value={values.pincode} onChange={change('pincode')} />
                
                {/* <TextField label="Country" value={values.country} onChange={change('country')} /> */}
                    <FormControl fullWidth size="small">
                    <InputLabel id="country-label">Country</InputLabel>
                    <Select
                        labelId="country-label"
                        id="country"
                        value={values.country || ""}
                        label="Country"
                        onChange={change('country')}
                    >
                        <MenuItem value="">
                        <em>Select Country</em>
                        </MenuItem>
                        <MenuItem value="USA">United States</MenuItem>
                    </Select>
                    </FormControl>
            </Stack>
            <FormControlLabel control={<Checkbox checked={!!values.is_primary} onChange={change('is_primary')} />} label="Primary" />
            <Button type="submit" variant="contained" disabled={submitting}>Save</Button>
        </Stack>
    </form>
)
}