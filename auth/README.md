
```bash
openssl genrsa -out jwt-private.pem 2048
```

```bash
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
