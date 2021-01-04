
# Owlet

Custom component for Home Assistant Core for monitoring Owlet smart sock.


## Installation

### With HACS
1. Open HACS Settings and add this repository 
as a Custom Repository (use **Integration** as the category).
2. The `Owlet` page should automatically load (or find it in the HACS Store)
3. Click `Install`

### Manual
Copy the `owlet` directory from `custom_components` in this repository,
and place inside your Home Assistant Core installation's `custom_components` directory.


## Setup
-----
```
owlet:
  username: (email)
  password: (password)
  name: (name)
```
