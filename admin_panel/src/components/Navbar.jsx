import { AppBar, Toolbar, Typography, IconButton, Box } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import LogoutIcon from '@mui/icons-material/Logout';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

function Navbar({ onMenuClick, onLogout }) {
    return (
        <AppBar position="sticky" elevation={0} sx={{ bgcolor: 'white', borderBottom: '1px solid #e0e0e0' }}>
            <Toolbar>
                <IconButton
                    edge="start"
                    color="primary"
                    onClick={onMenuClick}
                    sx={{ mr: 2, display: { sm: 'none' } }}
                >
                    <MenuIcon />
                </IconButton>

                <Typography variant="h6" color="primary" sx={{ flexGrow: 1, fontWeight: 600 }}>
                    Campus Bus Management
                </Typography>

                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <AccountCircleIcon color="action" />
                    <Typography variant="body2" color="text.secondary" sx={{ mr: 2 }}>
                        Admin
                    </Typography>
                    <IconButton color="error" onClick={onLogout} title="Logout">
                        <LogoutIcon />
                    </IconButton>
                </Box>
            </Toolbar>
        </AppBar>
    );
}

export default Navbar;
