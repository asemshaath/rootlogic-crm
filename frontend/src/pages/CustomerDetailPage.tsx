import * as React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Paper, Stack, Typography, Divider, Button, IconButton, Chip } from '@mui/material'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'
import AddIcon from '@mui/icons-material/Add'
import type { Customer, Address } from '../types'
import { getCustomer, updateCustomer, deleteCustomer, listAddresses, createAddress, updateAddress, deleteAddress } from '../api/customers'
import CustomerForm from '../components/CustomerForm'
import AddressForm from '../components/AddressForm'
import ConfirmDialog from '../components/ConfirmDialog'
import { useAppNotifications } from '../hooks/useAppNotifications'
import { useCallback, useEffect, useState } from 'react'

export default function CustomerDetailPage() {

    const { id } = useParams()
    const navigate = useNavigate()
    const { notify } = useAppNotifications()
    const [customer, setCustomer] = useState<Customer | null>(null)
    const [addresses, setAddresses] = useState<Address[]>([])
    const [primaryAddress, setPrimaryAddress] = useState<Address | null>(null)


    const [editing, setEditing] = useState(false)
    const [addingAddress, setAddingAddress] = useState(false)
    const [editingAddress, setEditingAddress] = useState<Address | null>(null)
    const [confirmCustomerDelete, setConfirmCustomerDelete] = useState(false)

    const load = useCallback(async () => {
        if (!id) return
        try {
            const c = await getCustomer(id)
            setCustomer(c)
            const addr = await listAddresses(id)
            setAddresses(addr.data)
            setPrimaryAddress(addr.primary_address ?? null)
        } catch (e: any) {
            notify(e.message, 'error')
        }
    }, [id, notify])

    useEffect(() => { load() }, [load])

    const handleUpdate = async (values: Partial<Customer>) => {
        if (!id) return
        try { 
            await updateCustomer(id, values); 
            notify('Customer updated', 'success'); 
            setEditing(false); 
            load() 
        } catch (e: any) { 
            notify(e.message, 'error') 
        }
    }


    const handleCustomerDelete = async () => {
        if (!id) return
        try { 
            await deleteCustomer(id); 
            notify('Customer deleted', 'success'); 
            navigate('/customers') 
        } catch (e: any) { 
            notify(e.message, 'error') 
        }
    }


    const handleCreateAddress = async (values: Partial<Address>) => {
        console.log("Creating address with values:", values);
        console.log("Customer ID:", id);
        if (!id) return
        try { 
            console.log("Calling createAddress API");
            await createAddress(id, values); 
            notify('Address added', 'success'); 
            setAddingAddress(false); 
            load() 
        } catch (e: any) { 
            notify(e.message, 'error') 
        }
    }


    const handleUpdateAddress = async (values: Partial<Address>) => {
        if (!id || !editingAddress) return
        try { 
            await updateAddress(id, editingAddress.id, values); 
            notify('Address updated', 'success'); 
            setEditingAddress(null); 
            load() 
        } catch (e: any) { 
            notify(e.message, 'error') 
        }
    }


    const handleDeleteAddress = async (addressId: string) => {
        if (!id) return
        try { 
            await deleteAddress(id, addressId); 
            notify('Address deleted', 'success'); 
            load() 
        } catch (e: any) { 
            notify(e.message, 'error') 
        }
    }


    if (!customer) return <Typography>Loading…</Typography>

    const onlyOneAddress = addresses.length === 1

    return (
        <Stack spacing={2}>
            <Paper sx={{ p: 2 }}>
                <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Stack>
                        <Typography variant="h5">{customer.first_name} {customer.last_name}</Typography>
                        <Typography variant="body2" color="text.secondary">{customer.email} · {customer.phone_number || '—'}</Typography>
                    </Stack>
                    <Stack direction="row" spacing={1}>
                        <Button startIcon={<EditIcon />} variant="outlined" onClick={() => setEditing((v) => !v)}>{editing ? 'Close' : 'Edit'}</Button>
                        <Button startIcon={<DeleteIcon />} color="error" variant="contained" onClick={() => setConfirmCustomerDelete(true)}>Delete</Button>
                    </Stack>
                </Stack>
                {onlyOneAddress && <Chip color="warning" label="Only One Address" sx={{ mt: 1 }} />}
                <Divider sx={{ my: 2 }} />
                {editing && <CustomerForm initial={customer} onSubmit={handleUpdate} />}
            </Paper>


            <Paper sx={{ p: 2 }}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                    <Typography variant="h6">Addresses ({addresses.length})</Typography>
                    <Button startIcon={<AddIcon />} variant="contained" onClick={() => setAddingAddress(true)}>Add Address</Button>
                </Stack>


                <Stack spacing={1}>
                    {addresses.map((a) => (
                    <Paper key={a.id} sx={{ p: 1.5 }} variant="outlined">
                        <Stack direction={{ xs: 'column', sm: 'row' }} justifyContent="space-between" alignItems={{ sm: 'center' }} spacing={1}>
                            <Stack>
                                <Typography variant="subtitle2">{a.address_line1}{a.address_line2 ? `, ${a.address_line2}` : ''}</Typography>
                                <Typography variant="body2" color="text.secondary">{a.city}, {a.state} {a.pincode}</Typography>
                            </Stack>
                            <Stack direction="row" spacing={1}>
                                {a.is_primary && <Chip size="small" color="success" label="Primary" />}
                                <IconButton onClick={() => setEditingAddress(a)} aria-label="edit"><EditIcon /></IconButton>
                                <IconButton color="error" onClick={() => handleDeleteAddress(a.id)} aria-label="delete"><DeleteIcon /></IconButton>
                            </Stack>
                        </Stack>
                    </Paper>
                    ))}
                </Stack>


                {addingAddress && (
                    <Paper sx={{ p: 2, mt: 2 }}>
                        <Typography variant="subtitle1" sx={{ mb: 1 }}>New Address</Typography>
                        <AddressForm onSubmit={handleCreateAddress} />
                        <Button sx={{ mt: 1 }} onClick={() => setAddingAddress(false)}>Close</Button>
                    </Paper>
                )}

                {editingAddress && (
                    <Paper sx={{ p: 2, mt: 2 }}>
                        <Typography variant="subtitle1" sx={{ mb: 1 }}>Edit Address</Typography>
                        <AddressForm initial={editingAddress} onSubmit={handleUpdateAddress} />
                        <Button sx={{ mt: 1 }} onClick={() => setEditingAddress(null)}>Close</Button>
                    </Paper>
                )}
            </Paper>


            <ConfirmDialog
                open={confirmCustomerDelete}
                title="Delete customer?"
                message="This action cannot be undone."
                onClose={() => setConfirmCustomerDelete(false)}
                onConfirm={handleCustomerDelete}
            />
        </Stack>
    )
}
