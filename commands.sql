--1-ый запрос
SELECT od.city,
       COUNT(*),
       AVG(ods.load_date - od.load_date) AS
FROM orders_deliveryrequest od
JOIN orders_deliverystatuscurrent ods ON od.internal_id = ods.internal_id_id
WHERE ods.status_name = 'Done'
GROUP BY od.city;

--2-ый запрос
SELECT ods.status_name, COUNT(*)
FROM orders_deliveryrequest od
JOIN orders_deliverystatuscurrent ods ON od.internal_id = ods.internal_id_id
WHERE od.package_type IN ('Письмо', 'Бандероль') 
      AND od.load_date >= now() - INTERVAL '3 weeks'
GROUP BY ods.status_name;

--3-ий запрос
SELECT od.package_type,
       odsh.status_name,
       AVG(EXTRACT(EPOCH FROM (odsh_next.load_date - odsh.load_date)))
FROM orders_deliveryrequest od
JOIN orders_deliveryrequeststatushistory odsh ON od.internal_id = odsh.internal_id_id
JOIN orders_deliveryrequeststatushistory odsh_next ON odsh.internal_id_id = odsh_next.internal_id_id
     AND odsh_next.load_date = (
         SELECT MIN(odsh2.load_date) 
         FROM orders_deliveryrequeststatushistory odsh2
         WHERE odsh2.internal_id_id = odsh.internal_id_id 
         AND odsh2.load_date > odsh.load_date
     )
WHERE od.city = 'Казань'
      AND odsh.internal_id_id IN (
          SELECT internal_id_id 
          FROM orders_deliverystatuscurrent 
          WHERE status_name = 'Done'
      )
GROUP BY od.package_type, odsh.status_name;
