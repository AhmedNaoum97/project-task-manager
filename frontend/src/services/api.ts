import axios from 'axios';

const API_URL = 'http://localhost:5000/api/v1';

const api = axios.create({
    baseURL: API_URL
});

// Add token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});


export const authService = {
    signup: (email: string, password: string) =>
        api.post('/auth/signup', { email, password }),
    login: (email: string, password: string) =>
        api.post('/auth/login', { email, password }),
        
}
export const taskService = {
    getTasks: () => api.get('/tasks'),
    createTask: (title: string, description?: string, priority?: string) =>
        api.post('/tasks', { title, description, priority }),
    updateTask: (id: string, data: any) => api.put(`/tasks/${id}`, data),
    deleteTask: (id: string) => api.delete(`/tasks/${id}`)
};