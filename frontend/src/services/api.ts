import axios from 'axios';
import type { CreateTaskPayload, UpdateTaskPayload } from '../types/task';

const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

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
    getTasks: (status?: string, priority?: string) => 
        api.get('/tasks', { params: { status, priority } }),
    getTask: (id: string) =>
        api.get(`/tasks/${id}`), 
    createTask: (data: CreateTaskPayload) =>
        api.post('/tasks', data),
    updateTask: (id: string, data: UpdateTaskPayload) =>
        api.put(`/tasks/${id}`, data),
    deleteTask: (id: string) =>
        api.delete(`/tasks/${id}`)
};