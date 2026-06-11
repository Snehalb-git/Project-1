use ola_project;
SELECT * FROM bookings 
WHERE Booking_Status = 'Success';



SELECT Vehicle_Type, AVG(Ride_Distance) AS Avg_Distance 
FROM bookings 
GROUP BY Vehicle_Type;



SELECT COUNT(*) AS Total_Cancelled_By_Customers 
FROM bookings 
WHERE Booking_Status = 'Cancelled by Customer';



SELECT Customer_ID, COUNT(Booking_ID) AS Total_Rides 
FROM bookings 
GROUP BY Customer_ID 
ORDER BY Total_Rides DESC 
LIMIT 5;



SELECT COUNT(*) AS Cancelled_By_Drivers_Issues 
FROM bookings 
WHERE Booking_Status = 'Cancelled by Driver' 
  AND (Reason_for_Cancelling_by_Driver = 'Personal & Car related issue' 
       OR Reason_for_Cancelling_by_Driver = 'Car Broken Down');
-- Note: 'Reason_for_Cancelling_by_Driver' cha exact column naav tumchya dataset nusar check kara.



SELECT MAX(Driver_Ratings) AS Max_Rating, MIN(Driver_Ratings) AS Min_Rating 
FROM bookings 
WHERE Vehicle_Type = 'Prime Sedan' 
  AND Driver_Ratings IS NOT NULL;


SELECT * FROM bookings 
WHERE Payment_Method = 'UPI';



SELECT Vehicle_Type, AVG(Customer_Rating) AS Avg_Customer_Rating 
FROM bookings 
GROUP BY Vehicle_Type;



SELECT SUM(Booking_Value) AS Total_Successful_Revenue 
FROM bookings 
WHERE Booking_Status = 'Success';



SELECT Booking_ID, Booking_Status, 
       Incomplete_Rides_Reason -- check exact column name for reason
FROM bookings 
WHERE Booking_Status = 'Incomplete' 
   OR Booking_Status = 'Cancelled by Customer' 
   OR Booking_Status = 'Cancelled by Driver';