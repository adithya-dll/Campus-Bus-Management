import { useState, useEffect } from 'react';
import {
    Box,
    Paper,
    Typography,
    Button,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    IconButton,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Chip,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { driversAPI } from '../services/api';

function Drivers() {
    const [drivers, setDrivers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [openDialog, setOpenDialog] = useState(false);
    const [currentDriver, setCurrentDriver] = useState(null);
    const [formData, setFormData] = useState({
        driver_id: '',
        name: '',
        email: '',
        phone: '',
        license_number: '',
        password: '',
    });

    useEffect(() => {
        fetchDrivers();
    }, []);

    const fetchDrivers = async () => {
        try {
            const response = await driversAPI.list();
            setDrivers(response.data.drivers || []);
        } catch (error) {
            console.error('Failed to fetch drivers:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAdd = () => {
        setCurrentDriver(null);
        setFormData({ driver_id: '', name: '', email: '', phone: '', license_number: '', password: '' });
        setOpenDialog(true);
    };

    const handleEdit = (driver) => {
        setCurrentDriver(driver);
        setFormData({
            driver_id: driver.driver_id,
            name: driver.name,
            email: driver.email || '',
            phone: driver.phone || '',
            license_number: driver.license_number || '',
            password: '',
        });
        setOpenDialog(true);
    };

    const handleSave = async () => {
        try {
            if (currentDriver) {
                const updateData = { ...formData };
                if (!updateData.password) delete updateData.password;
                await driversAPI.update(currentDriver.driver_id, updateData);
            } else {
                if (!formData.password) {
                    alert('Password is required for new drivers');
                    return;
                }
                await driversAPI.register(formData);
            }
            setOpenDialog(false);
            fetchDrivers();
        } catch (error) {
            console.error('Failed to save driver:', error);
            alert(error.response?.data?.error || 'Failed to save driver');
        }
    };

    const handleDelete = async (driverId) => {
        if (window.confirm('Are you sure you want to delete this driver?')) {
            try {
                await driversAPI.delete(driverId);
                fetchDrivers();
            } catch (error) {
                console.error('Failed to delete driver:', error);
            }
        }
    };

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <div className="spinner"></div>
            </Box>
        );
    }

    return (
        <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <div>
                    <Typography variant="h4" fontWeight="bold">
                        Drivers
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Manage driver accounts and assignments
                    </Typography>
                </div>
                <Button variant="contained" startIcon={<AddIcon />} onClick={handleAdd}>
                    Add Driver
                </Button>
            </Box>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Driver ID</TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>Email</TableCell>
                            <TableCell>Phone</TableCell>
                            <TableCell>License Number</TableCell>
                            <TableCell>Assigned Bus</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {drivers.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={8} align="center">
                                    <Typography color="text.secondary">No drivers found</Typography>
                                </TableCell>
                            </TableRow>
                        ) : (
                            drivers.map((driver) => (
                                <TableRow key={driver.driver_id}>
                                    <TableCell>{driver.driver_id}</TableCell>
                                    <TableCell>{driver.name}</TableCell>
                                    <TableCell>{driver.email || '-'}</TableCell>
                                    <TableCell>{driver.phone || '-'}</TableCell>
                                    <TableCell>{driver.license_number || '-'}</TableCell>
                                    <TableCell>{driver.assigned_bus || '-'}</TableCell>
                                    <TableCell>
                                        <Chip
                                            label={driver.is_active ? 'Active' : 'Inactive'}
                                            color={driver.is_active ? 'success' : 'default'}
                                            size="small"
                                        />
                                    </TableCell>
                                    <TableCell align="right">
                                        <IconButton size="small" onClick={() => handleEdit(driver)}>
                                            <EditIcon />
                                        </IconButton>
                                        <IconButton size="small" color="error" onClick={() => handleDelete(driver.driver_id)}>
                                            <DeleteIcon />
                                        </IconButton>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </TableContainer>

            <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
                <DialogTitle>{currentDriver ? 'Edit Driver' : 'Add Driver'}</DialogTitle>
                <DialogContent>
                    <TextField
                        fullWidth
                        label="Driver ID"
                        value={formData.driver_id}
                        onChange={(e) => setFormData({ ...formData, driver_id: e.target.value })}
                        margin="normal"
                        disabled={!!currentDriver}
                        required
                    />
                    <TextField
                        fullWidth
                        label="Name"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        margin="normal"
                        required
                    />
                    <TextField
                        fullWidth
                        label="Email"
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        label="Phone"
                        value={formData.phone}
                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                        margin="normal"
                        required
                    />
                    <TextField
                        fullWidth
                        label="License Number"
                        value={formData.license_number}
                        onChange={(e) => setFormData({ ...formData, license_number: e.target.value })}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        label={currentDriver ? "Password (leave blank to keep unchanged)" : "Password"}
                        type="password"
                        value={formData.password}
                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        margin="normal"
                        required={!currentDriver}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
                    <Button variant="contained" onClick={handleSave}>
                        Save
                    </Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
}

export default Drivers;
