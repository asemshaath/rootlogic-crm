# Rootlogic CRM

## Tech Stack:
Frontend: React + MUI

Backend: Python + Django + Django REST Framework

Database: Postgres hosted in a VM

# API Design Notes

## Customers List

GET `api/customers`
res: 
```js
{
    "count": 2,
    "data": [
        {**customer1, "num_of_addresses"},
        {**customer2, "num_of_addresses"}
    ]
}
```
---
POST 	`api/customers`

body: `{new_customer_info**}`

validation: validate the format of email, and phone_number. 

res: 
```js
{
    "id": "bd165cdf-401d-4e0e-abe2-f9b1b5d01a11",
    "first_name": "Asem",
    "last_name": "Shaath",
    "email": "shaathasem@gmail.com",
    "phone_number": "8005551234",
    "created_at": "2025-10-18T19:51:50.863058-05:00",
    "updated_at": "2025-10-18T19:51:50.863087-05:00",
    "organization": null
}
```

## Customer Details
GET 	`api/customers/<uuid>`

res:
```js
	{
        "id": "bd165cdf-401d-4e0e-abe2-f9b1b5d01a11",
        "first_name": "Asem",
        "last_name": "Shaath",
        ...
		"addresses": {
			"count": 2,
			"data": [{address1},{address2}],
			"primary_address": "address1"
		}
	}
```
---
PATCH	`api/customers/<uuid>`

body: 
```js
{"first_name": "Will", "last_name": "Smith"}
```

validation: validate the format of email, and phone_number. 

res: 
```js
	{
        "id": "bd165cdf-401d-4e0e-abe2-f9b1b5d01a11",
        "first_name": "Will",
        "last_name": "Smith",
        ...
		"addresses": {
			"count": 2,
			"data": [{address1},{address2}],
			"primary_address": "address1"
		}
	}
```
> Note: Edit only customer info NOT ADDRESS

---
DELETE	`api/customers/<uuid>`

res: 
```js
{
    "status": true,
    "message": "deleted the customer succesfully"
}
```
> Note: Cascade delete. Delete all assoctiated addresses.

## Addresses List
GET		`api/customers/<uuid>/addresses/`

res: 
```js
	{
		"count": 2,
		"data": [{address1}, {address2}],
		"full_primary_address": "address1",
		"primary_address": {city, state, country, pincode, street_line1}
	}
```
---
POST	`api/customers/<uuid>/addresses/`

To add a new address to the customer.

body: `{address_info**}`

validation: Validate if the address is in the correct format

> Note: When setting is_primary to true the other primary address must have is_primary=false 

res: `{new_address** full details}`

## Address Details
GET		`api/customers/<uuid>/addresses/<uuid>`

res:
```js
{
    "address_line1": "20 W 34th St",
    "address_line2": "",
    "city": "New York",
    "state": "NY",
    "pincode": "10118",
    "country": "USA",
    "is_primary": false,
    #etc..
}
```
---
PATCH `api/customers/<uuid>/addresses/<uuid>`

body: 
```js
{"address_line1": "21 W 34th St"}
```
validation: Validate if the entry is a valid format

res:
```js
{
    "address_line1": "21 W 34th St",
    "address_line2": "",
    "city": "New York",
    "state": "NY",
    "pincode": "10118",
    "country": "USA",
    "is_primary": false,
    #etc..
}
```
>Note: if `is_primary` changed to `false`, a random existing address will be set to primary. If the only address, it will fail.
---
DELETE `api/customers/<uuid>/addresses/<uuid>`

res: 
```js
{
    "status": true,
    "message": "deleted the address succesfully"
}
```

>Note: if primary address is deleted, a random existing address will be set to primary. If there are no addresses, proceed succesfully.


## Search
There will be the search term, in which, the user will pass the name, phone, or email. 

GET 	`api/customers/?search=(name, phone, email)`

For advance search. Example, search for all customers living in New York

GET 	`api/customers/?city=new york`

GET 	`api/customers/?state=NY`

GET 	`api/customers/?pincode=10103`
