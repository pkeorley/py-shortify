# py-shortify

`py-shortify` — is a link shortening service that provides a secure `API` for creating and managing shortened links. The service uses authentication tokens for authorization, which guarantees protection of all creation, update, and deletion operations from unauthorized access.

All authentication tokens are securely hashed using the `SHA-256` algorithm, which provides a reliable level of security in case of unauthorized access to data.


## Users

### GET `/api/v1/users`

Retrieves information about the authenticated user

#### Headers
```http
Authorization: Bearer {BASE64}
```

#### Response
```json
{
    "id": "{UUID}"
}
```

### POST `/api/v1/users`

Creates a new user

#### Response
```json
{
    "id": "{UUID}",
    "auth_token": "{BASE64}",
}
```


## Shortlinks

### GET `/api/v1/shortlinks`

Retrieves a list of all short links created by the users

#### Response

```json
[
    {
        "id": "{TEXT}",
        "name": "{TEXT}",
        "url": "{TEXT}"
    }
]
```

### GET `/api/v1/shortlinks/{name}`

Retrieves information about a specific short link by its name

#### Response
```json
{
    "id": "{UUID}",
    "name": "{TEXT}",
    "url": "{TEXT}"
}
```


## Shorten

### POST `/api/v1/shorten`

Creates a new short link

#### Headers
```http
Authorization: Bearer {AUTH_TOKEN}
```

#### Body

```json
{
    "name": "{TEXT}",
    "url": "{TEXT}"
}
```

#### Response

```json
{
    "id": "{UUID}"
}
```
