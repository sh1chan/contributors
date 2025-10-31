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
    - [x] /login
        - [x] `GET`
            - [x] Response Template
            - [x] Show ErrorMessage
        - [x] `POST`
            - [x] Validate User Credentials
                - [x] Required fields: `username`, `password`
                - [x] Use Password Hash to compare passwords
            - [x] Generate JWT with `expire` time
            - [x] Redirect user to the `issues` router
                - [x] Set `access_token` to the response cookies
    - [x] /logout
        - [x] `GET`
            - [x] Check if the User is logged in
            - [x] UnSet `access_token` from the response cookies
            - [x] Redirect user to the `issues` router
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
            - [x] Query Issues
                - [x] Sort Issues (by `creation_dt`)
            - [ ] Filter Issues
                - [ ] tags
                - [ ] labels
            - [x] No logging is required, so users can query `issues`
    - [ ] /add
        - [ ] `POST`
            - [x] User Required
            - [ ] Validate Issues URL
                - [x] Github
                    - [x] by netloc
                    - [ ] by path
                - [ ] Gitlab
            - [x] Redirect user to the `issues` router
                - [x] Add `error_message`
    - [ ] /create
        - [ ] `POST`
            - [ ] Validate
    - [ ] /{id}
    - [ ] /{id}/update
    - [ ] /{id}/delete
    - [ ] /{id}/vote

### Schemas