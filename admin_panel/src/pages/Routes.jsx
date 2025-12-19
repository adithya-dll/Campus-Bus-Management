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
    List,
    ListItem,
    ListItemText,
    MenuItem,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon, AddCircle as AddStopIcon } from '@mui/icons-material';
import { routesAPI, busesAPI } from '../services/api';

function Routes() {
    const [routes, setRoutes] = useState([]);
    const [buses, setBuses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [openDialog, setOpenDialog] = useState(false);
    const [currentRoute, setCurrentRoute] = useState(null);
    const [formData, setFormData] = useState({
        route_id: '',
        route_name: '',
        description: '',
        distance_km: 0,
        estimated_duration_minutes: 0,
        boarding_points: [],
    });
    const [newBoardingPoint, setNewBoardingPoint] = useState('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [routesRes, busesRes] = await Promise.all([
                routesAPI.list(),
                busesAPI.list(),
            ]);
            setRoutes(routesRes.data.routes || []);
            setBuses(busesRes.data.buses || []);
        } catch (error) {
            console.error('Failed to fetch data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAdd = () => {
        setCurrentRoute(null);
        setFormData({
            route_id: '',
            route_name: '',
            description: '',
            distance_km: 0,
            estimated_duration_minutes: 0,
            boarding_points: [],
        });
        setOpenDialog(true);
    };

    const handleEdit = (route) => {
        setCurrentRoute(route);
        setFormData({
            route_id: route.route_id,
            route_name: route.route_name,
            description: route.description || '',
            distance_km: route.distance_km || 0,
            estimated_duration_minutes: route.estimated_duration_minutes || 0,
            boarding_points: route.boarding_points || [],
        });
        setOpenDialog(true);
    };

    const handleAddBoardingPoint = () => {
        if (newBoardingPoint.trim()) {
            setFormData({
                ...formData,
                boarding_points: [...formData.boarding_points, newBoardingPoint.trim()],
            });
            setNewBoardingPoint('');
        }
    };

    const handleRemoveBoardingPoint = (index) => {
        setFormData({
            ...formData,
            boarding_points: formData.boarding_points.filter((_, i) => i !== index),
        });
    };

    const handleSave = async () => {
        try {
            if (currentRoute) {
                await routesAPI.update(currentRoute.route_id, formData);
            } else {
                await routesAPI.create(formData);
            }
            setOpenDialog(false);
            fetchData();
        } catch (error) {
            console.error('Failed to save route:', error);
            alert(error.response?.data?.error || 'Failed to save route');
        }
    };

    const handleDelete = async (routeId) => {
        if (window.confirm('Are you sure you want to delete this route?')) {
            try {
                await routesAPI.delete(routeId);
                fetchData();
            } catch (error) {
                console.error('Failed to delete route:', error);
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
                        Routes
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Manage bus routes and boarding points
                    </Typography>
                </div>
                <Button variant="contained" startIcon={<AddIcon />} onClick={handleAdd}>
                    Add Route
                </Button>
            </Box>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Route ID</TableCell>
                            <TableCell>Route Name</TableCell>
                            <TableCell>Assigned Bus</TableCell>
                            <TableCell>Boarding Points</TableCell>
                            <TableCell>Distance (km)</TableCell>
                            <TableCell>Duration (min)</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {routes.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={8} align="center">
                                    <Typography color="text.secondary">No routes found</Typography>
                                </TableCell>
                            </TableRow>
                        ) : (
                            routes.map((route) => (
                                <TableRow key={route.route_id}>
                                    <TableCell>{route.route_id}</TableCell>
                                    <TableCell>{route.route_name}</TableCell>
                                    <TableCell>{route.assigned_bus || '-'}</TableCell>
                                    <TableCell>
                                        {route.boarding_points?.length > 0
                                            ? `${route.boarding_points.length} stops`
                                            : '-'}
                                    </TableCell>
                                    <TableCell>{route.distance_km || 0}</TableCell>
                                    <TableCell>{route.estimated_duration_minutes || 0}</TableCell>
                                    <TableCell>
                                        <Chip
                                            label={route.is_active ? 'Active' : 'Inactive'}
                                            color={route.is_active ? 'success' : 'default'}
                                            size="small"
                                        />
                                    </TableCell>
                                    <TableCell align="right">
                                        <IconButton size="small" onClick={() => handleEdit(route)}>
                                            <EditIcon />
                                        </IconButton>
                                        <IconButton size="small" color="error" onClick={() => handleDelete(route.route_id)}>
                                            <DeleteIcon />
                                        </IconButton>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </TableContainer>

            <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
                <DialogTitle>{currentRoute ? 'Edit Route' : 'Add Route'}</DialogTitle>
                <DialogContent>
                    <TextField
                        fullWidth
                        label="Route ID"
                        value={formData.route_id}
                        onChange={(e) => setFormData({ ...formData, route_id: e.target.value })}
                        margin="normal"
                        disabled={!!currentRoute}
                        required
                    />
                    <TextField
                        fullWidth
                        label="Route Name"
                        value={formData.route_name}
                        onChange={(e) => setFormData({ ...formData, route_name: e.target.value })}
                        margin="normal"
                        required
                    />
                    <TextField
                        fullWidth
                        label="Description"
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        margin="normal"
                        multiline
                        rows={2}
                    />

                    <Box sx={{ mt: 3 }}>
                        <Typography variant="subtitle1" fontWeight="600" gutterBottom>
                            Boarding Points (Major Locations)
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                            <TextField
                                fullWidth
                                size="small"
                                label="Add boarding point"
                                value={newBoardingPoint}
                                onChange={(e) => setNewBoardingPoint(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && handleAddBoardingPoint()}
                                placeholder="e.g., Main Gate, Library, Hostel Block A"
                            />
                            <Button
                                variant="contained"
                                startIcon={<AddStopIcon />}
                                onClick={handleAddBoardingPoint}
                            >
                                Add
                            </Button>
                        </Box>
                        <List dense sx={{ bgcolor: '#f5f5f5', borderRadius: 1, maxHeight: 200, overflow: 'auto' }}>
                            {formData.boarding_points.length === 0 ? (
                                <ListItem>
                                    <ListItemText secondary="No boarding points added yet" />
                                </ListItem>
                            ) : (
                                formData.boarding_points.map((point, index) => (
                                    <ListItem
                                        key={index}
                                        secondaryAction={
                                            <IconButton edge="end" size="small" onClick={() => handleRemoveBoardingPoint(index)}>
                                                <DeleteIcon fontSize="small" />
                                            </IconButton>
                                        }
                                    >
                                        <ListItemText primary={`${index + 1}. ${point}`} />
                                    </ListItem>
                                ))
                            )}
                        </List>
                    </Box>

                    <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                        <TextField
                            label="Distance (km)"
                            type="number"
                            value={formData.distance_km}
                            onChange={(e) => setFormData({ ...formData, distance_km: parseFloat(e.target.value) })}
                            margin="normal"
                            fullWidth
                        />
                        <TextField
                            label="Estimated Duration (minutes)"
                            type="number"
                            value={formData.estimated_duration_minutes}
                            onChange={(e) => setFormData({ ...formData, estimated_duration_minutes: parseInt(e.target.value) })}
                            margin="normal"
                            fullWidth
                        />
                    </Box>
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

export default Routes;
