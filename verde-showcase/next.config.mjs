/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  allowedDevOrigins: ['*.e2b.app', '*.app.github.dev'],
  eslint: { ignoreDuringBuilds: true },
};

export default nextConfig;
