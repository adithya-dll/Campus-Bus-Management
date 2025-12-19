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
import { studentsAPI, busesAPI, routesAPI } from '../services/api';

function Students() {
    const [students, setStudents] = useState([]);
    const [buses, setBuses] = useState([]);
    const [routes, setRoutes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [openDialog, setOpenDialog] = useState(false);
    const [currentStudent, setCurrentStudent] = useState(null);
    const [formData, setFormData] = useState({
        roll_number: '',
        name: '',
        email: '',
        phone: '',
        assigned_bus: '',
        boarding_point: '',
    });
    const [availableBoardingPoints, setAvailableBoardingPoints] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    // Update boarding points when bus changes
    useEffect(() => {
        if (formData.assigned_bus) {
            const selectedBus = buses.find(b => b.bus_number === formData.assigned_bus);
            if (selectedBus && selectedBus.route_id) {
                const busRoute = routes.find(r => r.route_id === selectedBus.route_id);
                if (busRoute && busRoute.boarding_points) {
                    setAvailableBoardingPoints(busRoute.boarding_points);
                } else {
                    setAvailableBoardingPoints([]);
                }
            } else {
                setAvailableBoardingPoints([]);
            }
        } else {
            setAvailableBoardingPoints([]);
            setFormData(prev => ({ ...prev, boarding_point: '' }));
        }
    }, [formData.assigned_bus, buses, routes]);

    const fetchData = async () => {
        try {
            const [studentsRes, busesRes, routesRes] = await Promise.all([
                studentsAPI.list(),
                busesAPI.list(),
                routesAPI.list(),
            ]);
            setStudents(studentsRes.data.students || []);
            setBuses(busesRes.data.buses || []);
            setRoutes(routesRes.data.routes || []);
        } catch (error) {
            console.error('Failed to fetch data:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleAdd = () => {
        setCurrentStudent(null);
        setFormData({ roll_number: '', name: '', email: '', phone: '', assigned_bus: '', boarding_point: '' });
        setAvailableBoardingPoints([]);
        setOpenDialog(true);
    };

    const handleEdit = (student) => {
        setCurrentStudent(student);
        setFormData({
            roll_number: student.roll_number,
            name: student.name,
            email: student.email || '',
            phone: student.phone || '',
            assigned_bus: student.assigned_bus || '',
            boarding_point: student.boarding_point || '',
        });
        setOpenDialog(true);
    };

    const handleSave = async () => {
        try {
            if (currentStudent) {
                await studentsAPI.update(currentStudent.roll_number, formData);
            } else {
                await studentsAPI.add(formData);
            }
            setOpenDialog(false);
            fetchData();
        } catch (error) {
            console.error('Failed to save student:', error);
            alert(error.response?.data?.error || 'Failed to save student');
        }
    };

    const handleDelete = async (rollNumber) => {
        if (window.confirm('Are you sure you want to delete this student?')) {
            try {
                await studentsAPI.delete(rollNumber);
                fetchData();
            } catch (error) {
                console.error('Failed to delete student:', error);
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
                        Students
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        Manage student records and bus assignments
                    </Typography>
                </div>
                <Button variant="contained" startIcon={<AddIcon />} onClick={handleAdd}>
                    Add Student
                </Button>
            </Box>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Roll Number</TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>Email</TableCell>
                            <TableCell>Phone</TableCell>
                            <TableCell>Assigned Bus</TableCell>
                            <TableCell>Boarding Point</TableCell>
                            <TableCell>Pass Valid</TableCell>
                            <TableCell align="right">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {students.length === 0 ? (
                            <TableRow>
                                <TableCell colSpan={8} align="center">
                                    <Typography color="text.secondary">No students found</Typography>
                                </TableCell>
                            </TableRow>
                        ) : (
                            students.map((student) => (
                                <TableRow key={student.roll_number}>
                                    <TableCell><strong>{student.roll_number}</strong></TableCell>
                                    <TableCell>{student.name}</TableCell>
                                    <TableCell>{student.email || '-'}</TableCell>
                                    <TableCell>{student.phone || '-'}</TableCell>
                                    <TableCell>{student.assigned_bus || '-'}</TableCell>
                                    <TableCell>{student.boarding_point || '-'}</TableCell>
                                    <TableCell>
                                        <Chip
                                            label={student.bus_pass_valid ? 'Valid' : 'Invalid'}
                                            color={student.bus_pass_valid ? 'success' : 'error'}
                                            size="small"
                                        />
                                    </TableCell>
                                    <TableCell align="right">
                                        <IconButton size="small" onClick={() => handleEdit(student)}>
                                            <EditIcon />
                                        </IconButton>
                                        <IconButton size="small" color="error" onClick={() => handleDelete(student.roll_number)}>
                                            <DeleteIcon />
                                        </IconButton>
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Add/Edit Dialog */}
            <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
                <DialogTitle>{currentStudent ? 'Edit Student' : 'Add Student'}</DialogTitle>
                <DialogContent>
                    <TextField
                        fullWidth
                        label="Roll Number"
                        value={formData.roll_number}
                        onChange={(e) => setFormData({ ...formData, roll_number: e.target.value })}
                        margin="normal"
                        disabled={!!currentStudent}
                        required
                        helperText="Unique roll number (e.g., R2023001)"
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
                    />
                    <TextField
                        fullWidth
                        select
                        label="Assigned Bus"
                        value={formData.assigned_bus}
                        onChange={(e) => setFormData({ ...formData, assigned_bus: e.target.value })}
                        margin="normal"
                        required
                        helperText="Select the bus this student is assigned to"
                    >
                        <MenuItem value="">None</MenuItem>
                        {buses.map((bus) => (
                            <MenuItem key={bus.bus_number} value={bus.bus_number}>
                                {bus.bus_number} {bus.route_id ? `(Route: ${bus.route_id})` : ''}
                            </MenuItem>
                        ))}
                    </TextField>
                    <TextField
                        fullWidth
                        select
                        label="Boarding Point"
                        value={formData.boarding_point}
                        onChange={(e) => setFormData({ ...formData, boarding_point: e.target.value })}
                        margin="normal"
                        disabled={!formData.assigned_bus || availableBoardingPoints.length === 0}
                        helperText={
                            !formData.assigned_bus
                                ? "Select a bus first"
                                : availableBoardingPoints.length === 0
                                    ? "No boarding points available for this bus's route"
                                    : "Select your boarding point"
                        }
                    >
                        <MenuItem value="">None</MenuItem>
                        {availableBoardingPoints.map((point, index) => (
                            <MenuItem key={index} value={point}>
                                {point}
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

export default Students;
