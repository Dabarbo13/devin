import { ApolloClient, InMemoryCache, createHttpLink, ApolloLink, fromPromise } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { onError } from '@apollo/client/link/error';
// import { jwtDecode } from 'jwt-decode'; // Available if needed for proactive expiry checks

// HTTP link for GraphQL endpoint
const httpLink = createHttpLink({
  uri: import.meta.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8000/graphql/',
});

// Middleware to add JWT token to headers
const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('accessToken');
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : '',
    },
  };
});

// Function to get a new token
const getNewToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');
  if (!refreshToken) {
    // No refresh token available, clear session and redirect
    localStorage.removeItem('accessToken');
    localStorage.removeItem('user'); // refreshToken already null or removed
    window.location.href = '/#/login'; // Use hash router prefix
    return null;
  }

  try {
    const response = await fetch('http://localhost:8000/api/token/refresh/', { // Ensure this matches your backend URL
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    const data = await response.json();
    if (response.ok && data.access) {
      localStorage.setItem('accessToken', data.access);
      // Optional: If backend provides a new refresh token, update it as well
      // if (data.refresh) { localStorage.setItem('refreshToken', data.refresh); }
      return data.access;
    } else {
      // Refresh token failed or is invalid
      console.error('Token refresh failed:', data);
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      window.location.href = '/#/login'; // Use hash router prefix
      return null;
    }
  } catch (error) {
    console.error('Token refresh error:', error);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    window.location.href = '/#/login'; // Use hash router prefix
    return null;
  }
};

const errorLink = onError(({ graphQLErrors, networkError, operation, forward }) => {
  if (graphQLErrors) {
    for (let err of graphQLErrors) {
      // Handle specific GraphQL error codes if backend provides them for auth issues
      // Example: if (err.extensions?.code === 'UNAUTHENTICATED') { ... }
      // Depending on your backend, a 401 might also come as a GraphQL error.
      // For now, we primarily rely on networkError for 401s.
      console.warn('[GraphQL error]:', err);
    }
  }

  if (networkError) {
    // Check if the network error is a 401 Unauthorized error
    // Note: `networkError` structure can vary. `statusCode` is common with apollo-link-http.
    // If using fetch directly or other links, you might need to inspect `networkError.result.errors`
    // or `networkError.message`.
    const isAuthError = (networkError as any)?.statusCode === 401 || 
                        (networkError as any)?.result?.statusCode === 401 || 
                        (networkError as any)?.message?.includes('401');

    if (isAuthError) {
      console.log('[Network error]: 401 Unauthorized detected, attempting token refresh.');
      // If it's an auth error, try to refresh the token
      return fromPromise(
        getNewToken().then(newAccessToken => {
          if (newAccessToken) {
            console.log('[Token refresh]: Succeeded. Retrying original request.');
            // Modify the operation context with the new token
            const oldHeaders = operation.getContext().headers;
            operation.setContext({
              headers: {
                ...oldHeaders,
                authorization: `Bearer ${newAccessToken}`,
              },
            });
            // Retry the request
            return forward(operation);
          } else {
            console.log('[Token refresh]: Failed. User redirected to login.');
            // getNewToken() handles the redirect. No further action needed here for retry.
            // We must not forward the operation if token refresh failed.
            // Returning undefined or an error specific Observable could also work.
            return; 
          }
        }).catch(refreshError => {
          // This catch is for errors during the getNewToken() promise itself,
          // though getNewToken already has internal try/catch.
          console.error('[Token refresh]: Promise rejected.', refreshError);
          // Ensure logout and redirect if not already handled
          if (localStorage.getItem('accessToken') || localStorage.getItem('refreshToken')) {
             localStorage.removeItem('accessToken');
             localStorage.removeItem('refreshToken');
             localStorage.removeItem('user');
             window.location.href = '/#/login'; // Use hash router prefix
          }
          return; // Do not forward the operation
        })
      ).filter(value => Boolean(value)); // Ensure we don't forward if undefined is returned
    }
  }
});

// Chain the links: errorLink -> authLink -> httpLink
const client = new ApolloClient({
  link: errorLink.concat(authLink.concat(httpLink)),
  cache: new InMemoryCache(),
});

export default client;
