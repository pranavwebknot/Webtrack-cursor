export const theme = {
  colors: {
    primary: '#6B46C1',      // Webknot's purple brand color
    secondary: '#6C757D',    // Secondary text and icons
    background: {
      light: '#f8f9fa',
      dark: '#e9ecef',
    },
    text: {
      primary: '#2C3E50',
      secondary: '#6C757D',
      light: '#ADB5BD',
    },
    brand: {
      purple: '#6B46C1',     // Main brand color
      purpleLight: '#9F7AEA', // Lighter shade
      purpleDark: '#553C9A',  // Darker shade
    },
    success: '#28A745',
    warning: '#FFC107',
    error: '#DC3545',
    info: '#17A2B8',
  },
  typography: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    fontSize: {
      xs: '12px',
      sm: '14px',
      md: '16px',
      lg: '18px',
      xl: '24px',
      xxl: '32px',
    },
    fontWeight: {
      regular: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    round: '50%',
  },
  shadows: {
    sm: '0 2px 4px rgba(0, 0, 0, 0.05)',
    md: '0 4px 8px rgba(0, 0, 0, 0.1)',
    lg: '0 8px 16px rgba(0, 0, 0, 0.1)',
    xl: '0 12px 24px rgba(0, 0, 0, 0.1)',
  },
  transitions: {
    default: '0.2s ease',
    fast: '0.1s ease',
    slow: '0.3s ease',
  },
} as const;

export type Theme = typeof theme;
export default theme;
