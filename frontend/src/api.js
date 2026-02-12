/**
 * API helper: base URL and auth header from localStorage token.
 * Use for all authenticated requests so 401 can be handled in one place.
 */

const getAuthHeader = () => {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
};

/**
 * Fetch with auth. If response is 401, clears storage and returns null
 * so the app can redirect to login.
 */
export async function authFetch(url, options = {}) {
  const res = await fetch(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...getAuthHeader(), ...options.headers },
  });
  if (res.status === 401) {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    return null;
  }
  return res;
}

export { getAuthHeader };
