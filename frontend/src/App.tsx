import { Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom'
import { AppBar, Toolbar, Typography, Container, Box, IconButton, Tooltip, Snackbar, Alert } from '@mui/material'
import PeopleIcon from '@mui/icons-material/People'
import { useAppNotifications } from './hooks/useAppNotifications'
import CustomersPage from './pages/CustomersPage'
import CustomerDetailPage from './pages/CustomerDetailPage'


export default function App() {

  const { snackbar, closeSnackbar } = useAppNotifications()
  const navigate = useNavigate()

  return (
    <Box sx={{ minHeight: '100dvh', display: 'flex', flexDirection: 'column' }}>
      <AppBar position="sticky">
        <Toolbar>
          <Tooltip title="Customers">
            <IconButton color="inherit" onClick={() => navigate('/customers')}>
              <PeopleIcon />
            </IconButton>
          </Tooltip>
          <Typography variant="h6" sx={{ ml: 1, flexGrow: 1 }}>RootLogic CRM</Typography>
        </Toolbar>
      </AppBar>
      <Container sx={{ py: 3, flex: 1 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/customers" replace />} />
          <Route path="/customers" element={<CustomersPage />} />
          <Route path="/customers/:id" element={<CustomerDetailPage />} />
        </Routes>
      </Container>
      <Snackbar open={snackbar.open} autoHideDuration={4000} onClose={closeSnackbar}>
        <Alert severity={snackbar.severity} onClose={closeSnackbar} variant="filled">{snackbar.message}</Alert>
      </Snackbar>
    </Box>
  )
}