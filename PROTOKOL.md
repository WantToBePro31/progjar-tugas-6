### Register

`register [username] [password] [name] [country]`

- Tujuan: mendaftarkan data pengguna
- Parameter:
  - username: username pengguna
  - password: password pengguna
  - name: nama lengkap pengguna
  - country: negara pengguna

### Login

`auth [username] [password]`

- Tujuan: autentikasi pengguna terdaftar
- Parameter:
  - username: username pengguna terdaftar
  - password: password pengguna terdaftar

### Logout

`logout`

- Tujuan: keluar dari akun yang sedang login
- Parameter: -

### Send Private

`sendprivate [receiver] [message] `

- Tujuan: mengirimkan pesan secara privat
- Parameter:
  - receiver: nama penerima pesan
  - message: pesan yang dikirimkan

### Send Group

`sendgroup [group_receiver] [message]`

- Tujuan: mengirimkan pesan ke banyak orang
- Parameter:
  - group_receiver: nama-nama penerima pesan
  - message: pesan yang dikirimkan

### Inbox

`inbox`

- Tujuan: menampilkan pesan yang belum dibaca oleh pengguna
- Parameter: -

### Add Realm

`addrealm [realm_id] [realm_address_to] [realm_port_to]`

- Tujuan: menambahkan realm baru sebagai jembatan antara 2 server
- Parameter:
  - realm_id: nama realm yang menjadi identitas
  - realm_address_to: ip address dari server yang ingin dihubungkan
  - realm_port_to: port dari server yang ingin dihubungkan

### Send Private Realm

`sendprivaterealm [realm_id] [receiver] [message]`

- Tujuan: mengirimkan pesan secara privat ke pengguna yang terdapat pada server yang terhubung pada realm yang sama
- Parameter:
  - realm_id: nama realm yang menjadi identitas
  - receiver: nama penerima pesan
  - message: pesan yang dikirimkan

### Send Group Realm

`sendgrouprealm [realm_id] [group_receiver] [message]`

- Tujuan: mengirimkan pesan ke beberapa pengguna yang terdapat pada server yang terhubung pada realm yang sama
- Parameter:
  - realm_id: nama realm yang menjadi identitas
  - group_receiver: nama-nama penerima pesan

### Inbox Realm

`inboxrealm [realm_id]`

- Tujuan: menampilkan pesan yang belum dibaca oleh pengguna yang terdapat pada server yang terhubung pada realm yang sama
- Parameter:
  - realm_id: nama realm yang menjadi identitas

### Login Info

`logininfo`

- Tujuan: melihat info dari pengguna yang aktif
- Parameter: -
