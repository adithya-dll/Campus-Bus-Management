import { useState, useEffect } from 'react';
import { Box, Paper, Typography, Grid, Card, CardContent, Chip } from '@mui/material';
import { DirectionsBus as BusIcon } from '@mui/icons-material';
import { trackingAPI } from '../services/api';

function Tracking() {
    const [buses, setBuses] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchLocations();
        const interval = setInterval(fetchLocations, 5000); // Refresh every 5 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchLocations = async () => {
        try {
            const response = await trackingAPI.getAllLocations();
            setBuses(response.data.buses || []);
        } catch (error) {
            console.error('Failed to fetch locations:', error);
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

    return (
        <Box>
            <Typography variant="h4" fontWeight="bold" gutterBottom>
                Live Bus Tracking
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Real-time location of all active buses
            </Typography>

            <Grid container spacing={3}>
                {buses.length === 0 ? (
                    <Grid item xs={12}>
                        <Paper sx={{ p: 4, textAlign: 'center' }}>
                            <Typography color="text.secondary">No active buses found</Typography>
                        </Paper>
                    </Grid>
                ) : (
                    buses.map((bus) => (
                        <Grid item xs={12} sm={6} md={4} key={bus.bus_id}>
                            <Card>
                                <CardContent>
                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <BusIcon color="primary" />
                                            <Typography variant="h6">{bus.bus_number || bus.bus_id}</Typography>
                                        </Box>
                                        <Chip
                                            label={bus.trip_active ? 'On Trip' : 'Idle'}
                                            color={bus.trip_active ? 'success' : 'default'}
                                            size="small"
                                        />
                                    </Box>

                                    <Typography variant="body2" color="text.secondary" gutterBottom>
                                        Bus ID: {bus.bus_id}
                                    </Typography>

                                    {bus.driver_id && (
                                        <Typography variant="body2" color="text.secondary" gutterBottom>
                                            Driver: {bus.driver_id}
                                        </Typography>
                                    )}

                                    {bus.route_id && (
                                        <Typography variant="body2" color="text.secondary" gutterBottom>
                                            Route: {bus.route_id}
                                        </Typography>
                                    )}

                                    <Box sx={{ mt: 2, p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
                                        <Typography variant="caption" color="text.secondary" display="block">
                                            Last Location:
                                        </Typography>
                                        <Typography variant="body2">
                                            Lat: {bus.location?.lat?.toFixed(6) || 'N/A'}
                                        </Typography>
                                        <Typography variant="body2">
                                            Lng: {bus.location?.lng?.toFixed(6) || 'N/A'}
                                        </Typography>
                                        {bus.location?.timestamp && (
                                            <Typography variant="caption" color="text.secondary">
                                                Updated: {new Date(bus.location.timestamp).toLocaleTimeString()}
                                            </Typography>
                                        )}
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))
                )}
            </Grid>

            <Box sx={{ mt: 3, p: 2, bgcolor: '#fff3e0', borderRadius: 1 }}>
                <Typography variant="body2" color="text.secondary">
                    💡 Note: Google Maps integration for visual tracking can be added here
                </Typography>
            </Box>
        </Box>
    );
}

export default Tracking;
