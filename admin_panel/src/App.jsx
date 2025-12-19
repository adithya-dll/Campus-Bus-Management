import { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { Box } from '@mui/material';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Students from './pages/Students';
import Buses from './pages/Buses';
import RoutesPage from './pages/Routes';
import Drivers from './pages/Drivers';
import Tracking from './pages/Tracking';
import Logs from './pages/Logs';

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

// API
import { authAPI } from './services/api';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        try {
            const response = await authAPI.checkAuth();
            setIsAuthenticated(response.data.authenticated);
        } catch (error) {
            setIsAuthenticated(false);
        } finally {
            setLoading(false);
        }
    };

    const handleLogin = () => {
        setIsAuthenticated(true);
        navigate('/dashboard');
    };

    const handleLogout = async () => {
        try {
            await authAPI.logout();
            setIsAuthenticated(false);
            navigate('/login');
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    if (loading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <div className="spinner"></div>
            </Box>
        );
    }

    if (!isAuthenticated) {
        return (
            <Routes>
                <Route path="/login" element={<Login onLogin={handleLogin} />} />
                <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
        );
    }

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh' }}>
            <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
            <Box
                sx={{
                    flexGrow: 1,
                    display: 'flex',
                    flexDirection: 'column',
                    marginLeft: { xs: 0, sm: '260px' }, // Add margin to prevent overlap with permanent sidebar
                    transition: 'margin 0.3s ease',
                    width: { xs: '100%', sm: 'calc(100% - 260px)' }
                }}
            >
                <Navbar onMenuClick={() => setSidebarOpen(!sidebarOpen)} onLogout={handleLogout} />
                <Box component="main" sx={{ flexGrow: 1, p: 3, bgcolor: '#f5f5f5' }}>
                    <Routes>
                        <Route path="/dashboard" element={<Dashboard />} />
                        <Route path="/students" element={<Students />} />
                        <Route path="/buses" element={<Buses />} />
                        <Route path="/routes" element={<RoutesPage />} />
                        <Route path="/drivers" element={<Drivers />} />
                        <Route path="/tracking" element={<Tracking />} />
                        <Route path="/logs" element={<Logs />} />
                        <Route path="/" element={<Navigate to="/dashboard" replace />} />
                        <Route path="*" element={<Navigate to="/dashboard" replace />} />
                    </Routes>
                </Box>
            </Box>
        </Box>
    );
}

export default App;
