v0.1.0
------
- [ ] Auth
- [ ] Projects
- [ ] Issues


## TODO Checkbox
### Database
- [ ] Tables
    - [ ] User
        - [ ] Filters
        - [ ] Issues    ;; @type {added, followed, voted}
        - [ ] Projects  ;; @type {added, followed, voted}
    - [ ] Issues
        - [ ] Tags
        - [ ] Labels
        - [ ] Votes     ;; Filter
    - [ ] Tags
    - [ ] Labels

### App
- [x] Template Files
- [ ] Static Files

### Routers
- [ ] Auth
    - [x] /register
        - [x] `GET`
            - [x] Response Template
            - [x] Show ErrorMessage
        - [x] `POST`
            - [x] Validate User Credentials
                - [x] Required fields: `username`, `password`
                - [x] Unique fields: `username`
                - [x] Generate ErrorMessage
            - [x] Register User
                - [x] Save hashed `password`
            - [x] Redirect to the `login` page
    - [ ] /login
        - [x] `GET`
            - [x] Response Template
            - [x] Show ErrorMessage
        - [ ] `POST`
            - [ ] Validate User Credentials
                - [x] Required fields: `username`, `password`
                - [ ] Use Password Hash to compare passwords
            - [ ] Generate JWT with `expire` time
            - [ ] Set Auth Response Headers
    - [ ] /logoug
        - [ ] `POST`
    - [ ] /
    - [ ] /update
    - [ ] /delete
- [ ] Users
    - [ ] /
    - [ ] /{id}
- [ ] Teams
    - [ ] /
    - [ ] /create
    - [ ] /{id}
    - [ ] /{id}/update
    - [ ] /{id}/delete
- [ ] Projects
    - [ ] /
        - [ ] `GET`
    - [ ] /create
    - [ ] /{id}
    - [ ] /{id}/update
    - [ ] /{id}/delete
- [ ] Issues
    - [ ] /
        - [ ] `GET`
    - [ ] /create
    - [ ] /{id}
    - [ ] /{id}/update
    - [ ] /{id}/delete
    - [ ] /{id}/vote

### Schemas