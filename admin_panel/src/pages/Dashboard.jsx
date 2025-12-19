import { useState, useEffect } from 'react';
import { Grid, Paper, Typography, Box, Card, CardContent } from '@mui/material';
import {
    PeopleAlt as PeopleIcon,
    DirectionsBus as BusIcon,
    Person as DriverIcon,
    Warning as AlertIcon,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { logsAPI } from '../services/api';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

function StatCard({ title, value, icon, color }) {
    return (
        <Card sx={{ height: '100%' }}>
            <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                        <Typography color="text.secondary" gutterBottom variant="body2">
                            {title}
                        </Typography>
                        <Typography variant="h4" fontWeight="bold">
                            {value}
                        </Typography>
                    </Box>
                    <Box
                        sx={{
                            bgcolor: `${color}15`,
                            borderRadius: 2,
                            p: 1.5,
                            display: 'flex',
                            alignItems: 'center',
                        }}
                    >
                        {icon}
                    </Box>
                </Box>
            </CardContent>
        </Card>
    );
}

function Dashboard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchStatistics();
    }, []);

    const fetchStatistics = async () => {
        try {
            const response = await logsAPI.getStatistics();
            setStats(response.data);
        } catch (error) {
            console.error('Failed to fetch statistics:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <div className="spinner"></div>
            </Box>
        );
    }

    const systemStats = stats?.system_stats || {};
    const verificationStats = stats?.verification_stats || {};

    // Prepare data for charts
    const verificationData = Object.entries(verificationStats).map(([key, value]) => ({
        name: key.replace('_', ' '),
        count: value,
    }));

    return (
        <Box>
            <Typography variant="h4" fontWeight="bold" gutterBottom>
                Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                Overview of Campus Bus Management System
            </Typography>

            {/* Stats Cards */}
            <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Total Students"
                        value={systemStats.total_students || 0}
                        icon={<PeopleIcon sx={{ fontSize: 40, color: '#1976d2' }} />}
                        color="#1976d2"
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Total Buses"
                        value={systemStats.total_buses || 0}
                        icon={<BusIcon sx={{ fontSize: 40, color: '#2e7d32' }} />}
                        color="#2e7d32"
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Total Drivers"
                        value={systemStats.total_drivers || 0}
                        icon={<DriverIcon sx={{ fontSize: 40, color: '#9c27b0' }} />}
                        color="#9c27b0"
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Active Buses"
                        value={systemStats.active_buses || 0}
                        icon={<BusIcon sx={{ fontSize: 40, color: '#ed6c02' }} />}
                        color="#ed6c02"
                    />
                </Grid>
            </Grid>

            {/* Charts */}
            <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h6" fontWeight="600" gutterBottom>
                            Verification Statistics
                        </Typography>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={verificationData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="count" fill="#1976d2" />
                            </BarChart>
                        </ResponsiveContainer>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h6" fontWeight="600" gutterBottom>
                            System Status
                        </Typography>
                        <Box sx={{ mt: 2 }}>
                            <Box sx={{ mb: 2 }}>
                                <Typography variant="body2" color="text.secondary">
                                    Buses on Trip
                                </Typography>
                                <Typography variant="h5" fontWeight="bold">
                                    {systemStats.buses_on_trip || 0}
                                </Typography>
                            </Box>
                            <Box sx={{ mb: 2 }}>
                                <Typography variant="body2" color="text.secondary">
                                    Active Buses
                                </Typography>
                                <Typography variant="h5" fontWeight="bold" color="success.main">
                                    {systemStats.active_buses || 0}
                                </Typography>
                            </Box>
                            <Box>
                                <Typography variant="body2" color="text.secondary">
                                    Total Verifications
                                </Typography>
                                <Typography variant="h5" fontWeight="bold">
                                    {Object.values(verificationStats).reduce((a, b) => a + b, 0)}
                                </Typography>
                            </Box>
                        </Box>
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
}

export default Dashboard;
