import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import { login, logout, getCurrentUser } from '../store/slices/authSlice';
import type { LoginCredentials } from '../services/auth.service';

export const useAuth = () => {
  const dispatch = useDispatch();
  const { user, isAuthenticated, loading, error } = useSelector(
    (state: RootState) => state.auth
  );

  const handleLogin = async (credentials: LoginCredentials) => {
    return dispatch(login(credentials));
  };

  const handleLogout = () => {
    return dispatch(logout());
  };

  const fetchCurrentUser = () => {
    return dispatch(getCurrentUser());
  };

  return {
    user,
    isAuthenticated,
    loading,
    error,
    login: handleLogin,
    logout: handleLogout,
    getCurrentUser: fetchCurrentUser,
  };
};
