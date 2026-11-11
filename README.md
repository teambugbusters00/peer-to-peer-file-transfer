# Peer-to-Peer File Transfer

LAN file-sharing MVP built with FastAPI. Uploads receive random IDs and are stored in a local shared directory. Maximum upload size is 25 MB.

```bash
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --reload
```

Do not expose this unauthenticated service to the public internet. Add authentication, TLS, quotas, malware scanning, and expiry before real deployment.