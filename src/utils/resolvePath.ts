export const resolvePath = (path: string) => {
    if (!path) return '';
    if (path.startsWith('http')) return path;

    // Remove leading slash if it exists to avoid double slashes with BASE_URL
    const normalizedPath = path.startsWith('/') ? path.slice(1) : path;
    const baseUrl = import.meta.env.BASE_URL;

    // Ensure baseUrl ends with a slash
    const normalizedBaseUrl = baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`;

    return `${normalizedBaseUrl}${normalizedPath}`;
};
