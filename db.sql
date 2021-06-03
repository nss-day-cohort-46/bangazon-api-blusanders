insert into bangazonapi_favorite
(customer_id, seller_id)
VALUES
(5,6)

delete from bangazonapi_favorite where customer_id =5

select * from bangazonapi_favorite

SELECT
f.*,
u.last_name || ", " || u.first_name as cName

FROM bangazonapi_favorite f

JOIN bangazonapi_customer c on c.id = f.customer_id
JOIN auth_user u ON c.user_id = u.id
order by cName


SELECT
f.*,
u.last_name || ", " || u.first_name as cName,
s.last_name || ", " || s.first_name as sName

FROM bangazonapi_favorite f

JOIN bangazonapi_customer c on c.id = f.customer_id
JOIN auth_user u ON c.user_id = u.id
JOIN bangazonapi_customer cc on cc.id = f.seller_id
JOIN auth_user s ON cc.user_id = s.id
order by cName, sName