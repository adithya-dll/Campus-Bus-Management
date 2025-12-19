import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Important for session cookies
});

// Request interceptor
api.interceptors.request.use(
    (config) => {
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Redirect to login on unauthorized
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    login: (credentials) => api.post('/auth/login', credentials),
    logout: () => api.post('/auth/logout'),
    checkAuth: () => api.get('/auth/check'),
};

// Students API
export const studentsAPI = {
    list: (params) => api.get('/students/list', { params }),
    get: (id) => api.get(`/students/get/${id}`),
    add: (data) => api.post('/students/add', data),
    update: (id, data) => api.put(`/students/update/${id}`, data),
    delete: (id) => api.delete(`/students/delete/${id}`),
    registerFace: (id, formData) => api.post(`/students/register-face/${id}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    }),
};

// Buses API
export const busesAPI = {
    list: (params) => api.get('/buses/list', { params }),
    get: (id) => api.get(`/buses/get/${id}`),
    create: (data) => api.post('/buses/create', data),
    update: (id, data) => api.put(`/buses/update/${id}`, data),
    delete: (id) => api.delete(`/buses/delete/${id}`),
    assignDriver: (id, driverId) => api.put(`/buses/assign-driver/${id}`, { driver_id: driverId }),
    assignRoute: (id, routeId) => api.put(`/buses/assign-route/${id}`, { route_id: routeId }),
};

// Routes API
export const routesAPI = {
    list: (params) => api.get('/routes/list', { params }),
    get: (id) => api.get(`/routes/get/${id}`),
    create: (data) => api.post('/routes/create', data),
    update: (id, data) => api.put(`/routes/update/${id}`, data),
    delete: (id) => api.delete(`/routes/delete/${id}`),
};

// Drivers API
export const driversAPI = {
    list: (params) => api.get('/drivers/list', { params }),
    get: (id) => api.get(`/drivers/get/${id}`),
    register: (data) => api.post('/drivers/register', data),
    update: (id, data) => api.put(`/drivers/update/${id}`, data),
    delete: (id) => api.delete(`/drivers/delete/${id}`),
};

// Tracking API
export const trackingAPI = {
    getAllLocations: () => api.get('/tracking/get-all-locations'),
    getLocation: (busId) => api.get(`/tracking/get-location/${busId}`),
};

// Logs API
export const logsAPI = {
    getEntryLogs: (params) => api.get('/logs/entry', { params }),
    getAlerts: (params) => api.get('/logs/alerts', { params }),
    resolveAlert: (id) => api.put(`/logs/alerts/resolve/${id}`),
    getStatistics: (params) => api.get('/logs/statistics', { params }),
};

export default api;
