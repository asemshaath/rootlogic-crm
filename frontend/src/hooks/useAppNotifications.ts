import { useState, useCallback } from 'react'


export function useAppNotifications() {
    const [snackbar, setSnackbar] = useState<{ 
        open: boolean; 
        message: string; 
        severity: 'success'|'info'|'warning'|'error' }>({ open: false, message: '', severity: 'info' })
    const notify = useCallback((message: string, severity: 'success'|'info'|'warning'|'error' = 'info') => setSnackbar({ open: true, message, severity }), [])
    const closeSnackbar = useCallback(() => setSnackbar((s) => ({ ...s, open: false })), [])
    return { notify, snackbar, closeSnackbar }
}