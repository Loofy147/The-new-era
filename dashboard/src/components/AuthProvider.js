import React, { createContext, useContext, useState, useEffect } from 'react';
import { message } from 'antd';

// Authentication Context
const AuthContext = createContext();

// Authentication Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('access_token'));

  useEffect(() => {
    if (token) {
      fetchUserProfile();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchUserProfile = async () => {
    try {
      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        // Token is invalid, remove it
        localStorage.removeItem('access_token');
        setToken(null);
        setUser(null);
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
      // Clear invalid token
      localStorage.removeItem('access_token');
      setToken(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      setLoading(true);
      
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        const accessToken = data.access_token;
        
        // Store token
        localStorage.setItem('access_token', accessToken);
        setToken(accessToken);
        
        // Fetch user profile
        await fetchUserProfile();
        
        message.success('Login successful!');
        return { success: true };
      } else {
        const errorData = await response.json();
        message.error(errorData.detail || 'Login failed');
        return { success: false, error: errorData.detail };
      }
    } catch (error) {
      console.error('Login error:', error);
      message.error('Network error during login');
      return { success: false, error: 'Network error' };
    } finally {
      setLoading(false);
    }
  };

  const register = async (username, email, password) => {
    try {
      setLoading(true);
      
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password
        }),
      });

      if (response.ok) {
        const userData = await response.json();
        message.success('Registration successful! Please login.');
        return { success: true, user: userData };
      } else {
        const errorData = await response.json();
        message.error(errorData.detail || 'Registration failed');
        return { success: false, error: errorData.detail };
      }
    } catch (error) {
      console.error('Registration error:', error);
      message.error('Network error during registration');
      return { success: false, error: 'Network error' };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setToken(null);
    setUser(null);
    message.success('Logged out successfully');
  };

  const updateProfile = async (profileData) => {
    try {
      const response = await fetch('/api/auth/me', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(profileData),
      });

      if (response.ok) {
        const updatedUser = await response.json();
        setUser(updatedUser);
        message.success('Profile updated successfully');
        return { success: true, user: updatedUser };
      } else {
        const errorData = await response.json();
        message.error(errorData.detail || 'Profile update failed');
        return { success: false, error: errorData.detail };
      }
    } catch (error) {
      console.error('Profile update error:', error);
      message.error('Network error during profile update');
      return { success: false, error: 'Network error' };
    }
  };

  const isAuthenticated = () => {
    return !!(user && token);
  };

  const isAdmin = () => {
    return user?.is_admin || false;
  };

  const hasPermission = (permission) => {
    if (!user) return false;
    if (user.is_admin) return true;
    
    // Add custom permission logic here
    return user.permissions?.includes(permission) || false;
  };

  const getAuthHeaders = () => {
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };
  };

  const makeAuthenticatedRequest = async (url, options = {}) => {
    const authHeaders = getAuthHeaders();
    
    const response = await fetch(url, {
      ...options,
      headers: {
        ...authHeaders,
        ...options.headers,
      },
    });

    // Handle token expiration
    if (response.status === 401) {
      logout();
      window.location.href = '/login';
      return null;
    }

    return response;
  };

  const contextValue = {
    // State
    user,
    loading,
    token,
    
    // Actions
    login,
    register,
    logout,
    updateProfile,
    
    // Helpers
    isAuthenticated,
    isAdmin,
    hasPermission,
    getAuthHeaders,
    makeAuthenticatedRequest,
    
    // User data shortcuts
    userId: user?.id,
    username: user?.username,
    email: user?.email,
    displayName: user?.username || user?.email,
    isActive: user?.is_active,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Higher-order component for protected routes
export const withAuth = (WrappedComponent, options = {}) => {
  const { requireAdmin = false, redirectTo = '/login' } = options;
  
  return function AuthenticatedComponent(props) {
    const { isAuthenticated, isAdmin, loading } = useAuth();
    
    useEffect(() => {
      if (!loading && !isAuthenticated()) {
        window.location.href = redirectTo;
      } else if (!loading && requireAdmin && !isAdmin()) {
        message.error('Access denied: Admin privileges required');
        window.location.href = '/dashboard';
      }
    }, [loading, isAuthenticated, isAdmin]);
    
    if (loading) {
      return (
        <div className="flex-center" style={{ height: '100vh' }}>
          <div className="loading">Loading...</div>
        </div>
      );
    }
    
    if (!isAuthenticated()) {
      return null;
    }
    
    if (requireAdmin && !isAdmin()) {
      return null;
    }
    
    return <WrappedComponent {...props} />;
  };
};

// Hook for protected API calls
export const useApi = () => {
  const { makeAuthenticatedRequest, isAuthenticated } = useAuth();
  
  const get = (url, options = {}) => {
    return makeAuthenticatedRequest(url, { method: 'GET', ...options });
  };
  
  const post = (url, data, options = {}) => {
    return makeAuthenticatedRequest(url, {
      method: 'POST',
      body: JSON.stringify(data),
      ...options,
    });
  };
  
  const put = (url, data, options = {}) => {
    return makeAuthenticatedRequest(url, {
      method: 'PUT',
      body: JSON.stringify(data),
      ...options,
    });
  };
  
  const del = (url, options = {}) => {
    return makeAuthenticatedRequest(url, { method: 'DELETE', ...options });
  };
  
  return {
    get,
    post,
    put,
    delete: del,
    makeAuthenticatedRequest,
    isAuthenticated,
  };
};

export default AuthContext;
