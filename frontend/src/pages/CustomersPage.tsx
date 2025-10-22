import * as React from 'react'
import { useNavigate } from 'react-router-dom'
import { Paper, Stack, Typography, TextField, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TablePagination, IconButton, Divider, MenuItem, Select, InputLabel, FormControl } from '@mui/material'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'
import AddIcon from '@mui/icons-material/Add'
import { listCustomers, createCustomer, deleteCustomer } from '../api/customers'
import type { Customer } from '../types'
import CustomerForm from '../components/CustomerForm'
import ConfirmDialog from '../components/ConfirmDialog'
import { useAppNotifications } from '../hooks/useAppNotifications'
import { DataGrid } from '@mui/x-data-grid';
import { useEffect, useState } from 'react'
import { Alert, Snackbar } from '@mui/material'
import { Box} from '@mui/system'

export default function CustomersPage() {

    const [items, setItems] = useState<Customer[]>([])
    const [count, setCount] = useState(0)
    const [page, setPage] = useState(0)
    const [rowsPerPage, setRowsPerPage] = useState(10)
    const [loading, setLoading] = useState(false)
    const [search, setSearch] = useState('')
    const [city, setCity] = useState('')
    const [state, setState] = useState('')
    const [pincode, setPincode] = useState('')
    const [ordering, setOrdering] = useState('')

    const [paginationModel, setPaginationModel] = useState({
        page: 0,          
        pageSize: 10,
    });


    const [openCreate, setOpenCreate] = useState(false)
    const [toDelete, setToDelete] = useState<Customer | null>(null)


    const navigate = useNavigate()
    const { notify, snackbar, closeSnackbar } = useAppNotifications()


    const handleDelete = async () => {
        if (!toDelete) return

        try { 
            await deleteCustomer(toDelete.id); 
            notify('Customer deleted', 'success'); 
            setToDelete(null); 
            fetchData()
        }
        catch (e: any) { 
            notify(e.message, 'error') 
        }
    }

    const clearFilters = async () => { 
        await fetchData();
        setSearch(''); 
        setCity(''); 
        setState(''); 
        setPincode(''); 
        setPaginationModel((prev) => ({ ...prev, page: 0 }));
        // setTimeout(() => {
        //     fetchData();
        // }, 0);
    }

    const fetchData = async ()=>{
        setLoading(true)
        
        try {
            const { items, count } = await listCustomers({
                page: paginationModel.page + 1,
                page_size: paginationModel.pageSize,
                search: search || undefined,
                city: city || undefined,
                state: state || undefined,
                pincode: pincode || undefined,
            })
            
            // items.forEach((item, index) => {
            //     item.uuid = item.id; // DataGrid needs a `id` field
            //     item.id = index + paginationModel.page * paginationModel.pageSize;
            // });

            console.log(items);
            setItems(items)
            setCount(count)
        } catch (e: any) {
            notify(e.message || 'Failed to load customers', 'error')
        } finally {
            setLoading(false)
        }
    }


    useEffect(()=>{
        
        const fetchDataAsync = async () => {
            await fetchData();
        };

        fetchDataAsync();

    }, [paginationModel, search, notify]);

    const handleCreate = async (values: Partial<Customer>) => {
        console.log("handleCreate called with:", values)

        try { 
            const res = await createCustomer(values); 
            setOpenCreate(false); 
            console.log(res);
            notify('Customer created', 'success'); 
            fetchData() 
        }
        catch (e: any) { 
            notify(e.message, 'error') 
        }
    }

    const columns: any = [
            { field: 'first_name', headerName: 'First name', width: 150 },
            { field: 'last_name', headerName: 'Last name', width: 150 },
            { field: 'email', headerName: 'Email', width: 200 },
            { field: 'phone_number', headerName: 'Phone', width: 150 },
            { field: 'has_only_primary_address', headerName: 'Primary Address Only', width: 180, type: 'boolean' },
            { field: 'actions', headerName: 'Actions', width: 200, renderCell: (params: any) => (
                <>
                    <IconButton onClick={() => navigate(`/customers/${params.row.id}`)} aria-label="edit"><EditIcon /></IconButton>
                    <IconButton color="error" onClick={() => setToDelete(params.row)} aria-label="delete"><DeleteIcon /></IconButton>
                </>
            ) },
    ];

    return (        
            <Box sx={{ width: '100%', p: 2 }}>
            <Paper sx={{ p: 2, mb: 2 }}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                Customer Search
                </Typography>

                <TextField
                label="Search (name/email/phone)"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                fullWidth
                sx={{ mb: 2 }}
                />

                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} sx={{ mb: 2 }}>
                <TextField
                    label="City"
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    fullWidth
                />
                <TextField
                    label="State"
                    value={state}
                    onChange={(e) => setState(e.target.value)}
                    fullWidth
                />
                <TextField
                    label="Pincode"
                    value={pincode}
                    onChange={(e) => setPincode(e.target.value)}
                    fullWidth
                />
                <Stack direction="row" spacing={1}>
                    <Button variant="outlined" onClick={clearFilters}>Clear</Button>
                    <Button
                    variant="contained"
                    onClick={async () => await fetchData()}
                    >
                    Apply
                    </Button>
                </Stack>
                </Stack>
            </Paper>

            <Paper sx={{ p: 2 }}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                <Typography variant="h6">Customers</Typography>
                <Button
                    startIcon={<AddIcon />}
                    variant="contained"
                    onClick={() => setOpenCreate(true)}
                >
                    New Customer
                </Button>
                </Stack>

                <div style={{ height: 500, width: '100%' }}>
                <DataGrid
                    rows={items}
                    columns={columns}
                    rowCount={count}
                    paginationMode="server"
                    paginationModel={paginationModel}
                    getRowId={(row) => row.id} // Use the backend UUID directly
                    onPaginationModelChange={setPaginationModel}
                    pageSizeOptions={[5, 10, 25]}
                    loading={loading}
                />
                </div>
            </Paper>

            {/* 🗑 Confirm Delete Dialog */}
            <ConfirmDialog
                open={!!toDelete}
                title="Delete customer?"
                message={`This will remove ${toDelete?.first_name} ${toDelete?.last_name}.`}
                onClose={() => setToDelete(null)}
                onConfirm={handleDelete}
            />

            {/* 🔔 Snackbar Notifications */}
            <Snackbar
                open={snackbar.open}
                autoHideDuration={2000}
                onClose={closeSnackbar}
            >
                <Alert onClose={closeSnackbar} severity={snackbar.severity}>
                {snackbar.message}
                </Alert>
            </Snackbar>

            {/* 🧾 Create Form Drawer */}
            {openCreate && (
                <Paper sx={{ p: 3, mt: 2 }}>
                <Typography variant="h6" sx={{ mb: 1 }}>
                    Create Customer
                </Typography>
                <CustomerForm onSubmit={handleCreate} />
                <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
                    <Button onClick={() => setOpenCreate(false)}>Close</Button>
                </Stack>
                </Paper>
            )}
            </Box>
        );
}