import { useState } from 'react';
import {
    Box,
    Card,
    CardContent,
    TextField,
    Button,
    Typography,
    Alert,
    Container,
} from '@mui/material';
import DirectionsBusIcon from '@mui/icons-material/DirectionsBus';
import { authAPI } from '../services/api';

function Login({ onLogin }) {
    const [formData, setFormData] = useState({
        user_id: 'admin',
        password: 'admin123',
        user_type: 'admin',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await authAPI.login(formData);
            if (response.data) {
                onLogin();
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box
            sx={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            }}
        >
            <Container maxWidth="sm">
                <Card
                    sx={{
                        p: 4,
                        borderRadius: 4,
                        boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
                    }}
                >
                    <CardContent>
                        <Box sx={{ textAlign: 'center', mb: 4 }}>
                            <DirectionsBusIcon sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
                            <Typography variant="h4" fontWeight="bold" gutterBottom>
                                Campus Bus Management
                            </Typography>
                            <Typography variant="body1" color="text.secondary">
                                Admin Panel
                            </Typography>
                        </Box>

                        {error && (
                            <Alert severity="error" sx={{ mb: 3 }}>
                                {error}
                            </Alert>
                        )}

                        <form onSubmit={handleSubmit}>
                            <TextField
                                fullWidth
                                label="User ID"
                                value={formData.user_id}
                                onChange={(e) => setFormData({ ...formData, user_id: e.target.value })}
                                margin="normal"
                                required
                                autoFocus
                            />
                            <TextField
                                fullWidth
                                label="Password"
                                type="password"
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                margin="normal"
                                required
                            />
                            <Button
                                type="submit"
                                variant="contained"
                                fullWidth
                                size="large"
                                disabled={loading}
                                sx={{
                                    mt: 3,
                                    py: 1.5,
                                    fontSize: '1.1rem',
                                    textTransform: 'none',
                                    fontWeight: 600,
                                }}
                            >
                                {loading ? 'Logging in...' : 'Login'}
                            </Button>
                        </form>

                        <Typography variant="caption" display="block" textAlign="center" sx={{ mt: 3 }} color="text.secondary">
                            Default credentials: admin / admin123
                        </Typography>
                    </CardContent>
                </Card>
            </Container>
        </Box>
    );
}

export default Login;
