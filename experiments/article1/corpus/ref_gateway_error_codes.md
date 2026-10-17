# Harborline Gateway Error Code Catalog

Fictional evaluation document; it describes no real organization, person, or product.

Each entry lists the code, its meaning, and the recommended client action.

- HX-1447: The upstream TLS handshake timed out. Retry with exponential backoff.
- HX-1474: The client certificate has expired. Renew the certificate and reconnect.
- HX-4147: The request body exceeded the 10 MB limit. Split the payload into smaller requests.
- HX-4417: The tenant quota for the current billing period is exhausted. Ask the account owner to raise the quota.
- HX-4471: The API key was revoked by an administrator. Issue a new key from the console.
- HX-4714: The API key is valid but lacks the required scope. Add the scope in the console.
- HX-7140: The per-minute rate limit was exceeded. Wait for the interval shown in the Retry-After header.
- HX-7401: The idempotency key was reused with a different payload. Generate a new idempotency key.
- HX-7410: The webhook signature did not match. Verify the signing secret configured for the endpoint.
- HX-7104: The webhook endpoint returned a non-2xx status five times in a row and was disabled. Fix the endpoint and re-enable it.
