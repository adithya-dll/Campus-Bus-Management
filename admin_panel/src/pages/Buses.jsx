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
    MenuItem,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { busesAPI, driversAPI, routesAPI } from '../services/api';

function Buses() {
    const [buses, setBuses] = useState([]);
    const [drivers, setDrivers] = useState([]);
    const [routes, setRoutes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [openDialog, setOpenDialog] = useState(false);
    const [currentBus, setCurrentBus] = useState(null);
    const [formData, setFormData] = useState({
        bus_number: '',
        capacity: 50,
        driver_id: '',
        route_id: '',
        is_active: true,
    });

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [busesRes, driversRes, routesRes] = await Promise.all([
                busesAPI.list(),
                driversAPI.list(),
                routesAPI.list(),
            ]);
            setBuses(busesRes.data.buses || []);
            setDrivers(driversRes.data.drivers || []);
            setRoutes(routesRes.data.routes || []);
        } catch (error) {
            console.error('Failed to fetch data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAdd = () => {
        setCurrentBus(null);
        setFormData({ bus_number: '', capacity: 50, driver_id: '', route_id: '', is_active: true });
        setOpenDialog(true);
    };

    const handleEdit = (bus) => {
        setCurrentBus(bus);
        setFormData({
            bus_number: bus.bus_number,
            capacity: bus.capacity || 50,
            driver_id: bus.driver_id || '',
            route_id: bus.route_id || '',
            is_active: bus.is_active !== false,
        });
        setOpenDialog(true);
    };

    const handleSave = async () => {
        try {
            if (currentBus) {
                await busesAPI.update(currentBus.bus_number, formData);
            } else {
                await busesAPI.create(formData);
            }
            setOpenDialog(false);
            fetchData();
        } catch (error) {
            console.error('Failed to save bus:', error);
            alert(error.response?.data?.error || 'Failed to save bus');
        }
    };

    const handleDelete = async (busNumber) => {
        if (window.confirm('Are you sure you want to delete this bus?')) {
            try {
                await busesAPI.delete(busNumber);
                fetchData();
            } catch (error) {
                console.error('Failed to delete bus:', error);
            }
        }
    };

    const getDriverName = (driverId) => {
        const driver = drivers.find(d => d.driver_id === driverId);
        return driver ? driver.name : '-';
    };

    const getRouteName = (routeId) => {
        const route = routes.find(r => r.route_id === routeId);
        return route ? route.route_name : '-';
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
                        Buses
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Manage bus fleet and assignments
                    </Typography>
                </div>
                <Button variant="contained" startIcon={<AddIcon />} onClick={handleAdd}>
                    Add Bus
                </Button>
            </Box>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Bus Number</TableCell>
                            <TableCell>Capacity</TableCell>
                            <TableCell>Assigned Driver</TableCell>
                            <TableCell>Assigned Route</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell>Trip Active</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {buses.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={7} align="center">
                                    <Typography color="text.secondary">No buses found</Typography>
                                </TableCell>
                            </TableRow>
                        ) : (
                            buses.map((bus) => (
                                <TableRow key={bus.bus_number}>
                                    <TableCell><strong>{bus.bus_number}</strong></TableCell>
                                    <TableCell>{bus.capacity || 50}</TableCell>
                                    <TableCell>{getDriverName(bus.driver_id)}</TableCell>
                                    <TableCell>{getRouteName(bus.route_id)}</TableCell>
                                    <TableCell>
                                        <Chip
                                            label={bus.is_active ? 'Active' : 'Inactive'}
                                            color={bus.is_active ? 'success' : 'default'}
                                            size="small"
                                        />
                                    </TableCell>
                                    <TableCell>
                                        <Chip
                                            label={bus.trip_active ? 'On Trip' : 'Idle'}
                                            color={bus.trip_active ? 'warning' : 'default'}
                                            size="small"
                                        />
                                    </TableCell>
                                    <TableCell align="right">
                                        <IconButton size="small" onClick={() => handleEdit(bus)}>
                                            <EditIcon />
                                        </IconButton>
                                        <IconButton size="small" color="error" onClick={() => handleDelete(bus.bus_number)}>
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
                <DialogTitle>{currentBus ? 'Edit Bus' : 'Add Bus'}</DialogTitle>
                <DialogContent>
                    <TextField
                        fullWidth
                        label="Bus Number"
                        value={formData.bus_number}
                        onChange={(e) => setFormData({ ...formData, bus_number: e.target.value })}
                        margin="normal"
                        disabled={!!currentBus}
                        required
                        helperText="Unique bus number (e.g., KA01AB1234)"
                    />
                    <TextField
                        fullWidth
                        label="Capacity"
                        type="number"
                        value={formData.capacity}
                        onChange={(e) => setFormData({ ...formData, capacity: parseInt(e.target.value) })}
                        margin="normal"
                    />
                    <TextField
                        fullWidth
                        select
                        label="Assigned Driver"
                        value={formData.driver_id}
                        onChange={(e) => setFormData({ ...formData, driver_id: e.target.value })}
                        margin="normal"
                    >
                        <MenuItem value="">None</MenuItem>
                        {drivers.map((driver) => (
                            <MenuItem key={driver.driver_id} value={driver.driver_id}>
                                {driver.name} ({driver.driver_id})
                            </MenuItem>
                        ))}
                    </TextField>
                    <TextField
                        fullWidth
                        select
                        label="Assigned Route"
                        value={formData.route_id}
                        onChange={(e) => setFormData({ ...formData, route_id: e.target.value })}
                        margin="normal"
                    >
                        <MenuItem value="">None</MenuItem>
                        {routes.map((route) => (
                            <MenuItem key={route.route_id} value={route.route_id}>
                                {route.route_name} ({route.route_id})
                            </MenuItem>
                        ))}
                    </TextField>
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

export default Buses;
