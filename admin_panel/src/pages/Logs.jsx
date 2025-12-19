import { useState, useEffect } from 'react';
import {
    Box,
    Paper,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Chip,
    Tabs,
    Tab,
    TextField,
} from '@mui/material';
import { logsAPI } from '../services/api';

function Logs() {
    const [tabValue, setTabValue] = useState(0);
    const [entryLogs, setEntryLogs] = useState([]);
    const [alerts, setAlerts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [logsRes, alertsRes] = await Promise.all([
                logsAPI.getEntryLogs(),
                logsAPI.getAlerts(),
            ]);
            setEntryLogs(logsRes.data.logs || []);
            setAlerts(alertsRes.data.alerts || []);
        } catch (error) {
            console.error('Failed to fetch logs:', error);
        } finally {
            setLoading(false);
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'valid':
                return 'success';
            case 'invalid_pass':
                return 'warning';
            case 'not_found':
            case 'invalid_no_face':
                return 'error';
            default:
                return 'default';
        }
    };

    const getSeverityColor = (severity) => {
        switch (severity) {
            case 'high':
                return 'error';
            case 'medium':
                return 'warning';
            case 'low':
                return 'info';
            default:
                return 'default';
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
                Logs & Reports
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                View entry verification logs and security alerts
            </Typography>

            <Paper sx={{ mb: 3 }}>
                <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
                    <Tab label={`Entry Logs (${entryLogs.length})`} />
                    <Tab label={`Alerts (${alerts.length})`} />
                </Tabs>
            </Paper>

            {tabValue === 0 && (
                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Timestamp</TableCell>
                                <TableCell>Student ID</TableCell>
                                <TableCell>Student Name</TableCell>
                                <TableCell>Bus ID</TableCell>
                                <TableCell>Driver ID</TableCell>
                                <TableCell>Status</TableCell>
                                <TableCell>Confidence</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {entryLogs.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={7} align="center">
                                        <Typography color="text.secondary">No entry logs found</Typography>
                                    </TableCell>
                                </TableRow>
                            ) : (
                                entryLogs.map((log, index) => (
                                    <TableRow key={index}>
                                        <TableCell>{new Date(log.timestamp).toLocaleString()}</TableCell>
                                        <TableCell>{log.student_id || '-'}</TableCell>
                                        <TableCell>{log.student_name || '-'}</TableCell>
                                        <TableCell>{log.bus_id}</TableCell>
                                        <TableCell>{log.driver_id || '-'}</TableCell>
                                        <TableCell>
                                            <Chip
                                                label={log.status}
                                                color={getStatusColor(log.status)}
                                                size="small"
                                            />
                                        </TableCell>
                                        <TableCell>
                                            {log.confidence ? `${(log.confidence * 100).toFixed(1)}%` : '-'}
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}

            {tabValue === 1 && (
                <TableContainer component={Paper}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Timestamp</TableCell>
                                <TableCell>Alert Type</TableCell>
                                <TableCell>Severity</TableCell>
                                <TableCell>Bus ID</TableCell>
                                <TableCell>Message</TableCell>
                                <TableCell>Status</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {alerts.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={6} align="center">
                                        <Typography color="text.secondary">No alerts found</Typography>
                                    </TableCell>
                                </TableRow>
                            ) : (
                                alerts.map((alert, index) => (
                                    <TableRow key={index}>
                                        <TableCell>{new Date(alert.timestamp).toLocaleString()}</TableCell>
                                        <TableCell>{alert.alert_type}</TableCell>
                                        <TableCell>
                                            <Chip
                                                label={alert.severity}
                                                color={getSeverityColor(alert.severity)}
                                                size="small"
                                            />
                                        </TableCell>
                                        <TableCell>{alert.bus_id || '-'}</TableCell>
                                        <TableCell>{alert.message}</TableCell>
                                        <TableCell>
                                            <Chip
                                                label={alert.resolved ? 'Resolved' : 'Open'}
                                                color={alert.resolved ? 'default' : 'warning'}
                                                size="small"
                                            />
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}
        </Box>
    );
}

export default Logs;
