select * from bangazonapi_recommendation

insert into 
bangazonapi_recommendation
(customer_id, product_id, recommender_id)
values (4,22,5)

select * from authtoken_token



SELECT
    o.*,
    u.first_name, u.last_name

FROM
    bangazonapi_order o
JOIN
    bangazonapi_customer c ON o.customer_id = c.id
JOIN
    bangazonapi_orderproduct op on op.order_id = o.id 
JOIN
    bangazonapi_product p on op.product_id = p.id 
JOIN
    auth_user u ON c.user_id = u.id

where payment_type_id is not NULL
