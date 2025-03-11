import React from 'react';

interface WebknotLogoProps {
  width?: number;
  height?: number;
  color?: string;
}

const WebknotLogo: React.FC<WebknotLogoProps> = ({
  width = 48,
  height = 48,
  color = '#6B46C1' // Default purple color
}) => {
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 1000 1000"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g transform="translate(100, 100) scale(0.8)">
        {/* Left triangle */}
        <path
          d="M200 600 L500 200 L500 600 Z"
          fill={color}
          opacity="0.8"
        />
        {/* Center triangle */}
        <path
          d="M400 600 L500 200 L600 600 Z"
          fill={color}
          opacity="0.9"
        />
        {/* Right triangle */}
        <path
          d="M500 600 L500 200 L800 600 Z"
          fill={color}
          opacity="0.8"
        />
      </g>
    </svg>
  );
};

export default WebknotLogo;
