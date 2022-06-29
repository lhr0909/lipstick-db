/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  images: {
    domains: ['s1.vika.cn'],
  },
}

module.exports = nextConfig
