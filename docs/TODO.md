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
    - [ ] /register
        - [x] `GET`
            - [x] Response Template
        - [ ] `POST`
            - [ ] Register User
            - [ ] Redirect to the `login` page
    - [ ] /login
        - [ ] `GET`
            - [ ] Response Template
        - [ ] `POST`
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