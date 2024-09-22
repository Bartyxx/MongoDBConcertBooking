<!-- ---------------------------------------------------------------------- -->
<h1>MongoDBConcertBooking</h1>
<!-- ---------------------------------------------------------------------- -->

Welcome to the Python application for booking concerts!<br/>
The concert informations are stored in a MongoDB database composed of 4 collections:<br/>

<ul>
<li>concert  </li>
<li>tickets  </li>
<li>services </li>
<li>users    </li>
</ul>

Python interacts with MongoDB through queries that return the data requested 
by users or modify the data in the database.

<br/>
<h2>Python</h2>
<br/>

Users must register in the application to buy tickets. After entering their 
first name, last name, and tax code, they will be registered. It is important 
to use a unique tax code because it serves as the primary key in the database. 
If a user enters a tax code that is already registered, the registration will 
fail.<br/>

It's possible to filter by:<br/>

<ul>
<li>artist       </li>
<li>date         </li>
<li>city         </li>
<li>concert name </li>
</ul>

After selecting a concert based on these filters, users can proceed to buy 
tickets.<br/>
Typically, 4 seating options are available:<br/>
<p><img src = "https://github.com/Bartyxx/MongoDBConcertBooking/blob/main/img/sector.png"/></p>

After selecting the seating option and the number of tickets, the total cost of
the transaction will be displayed, and the database will be updated with the 
new number of available tickets.<br/>
<p><img src = "https://github.com/Bartyxx/MongoDBConcertBooking/blob/main/img/tickets.png"/></p>

Finally, a list of services near the concert location will be shown.<br/>
<p><img src = "https://github.com/Bartyxx/MongoDBConcertBooking/blob/main/img/services.png"/></p>

<br/>
<h2>Function</h2>
<br/>

Each filter is associated with a function that interacts with MongoDB and 
returns the results chosen by the users.<br/>

<ul>
<li>filter_by_artist       </li>
<li>filter_by_city         </li>
<li>filter_by_concert_name </li>
<li>filter_by_date         </li>
</ul>

<br/>
<h2>Query</h2>
<br/>

Each database is initialized with a variable, and these variables are used to 
interact with the collections in the program.<br/>

<pre>
self.db_users = self.client.exam.users
self.db_tickets = self.client.exam.tickets
self.db_concerts = self.client.exam.concerts
self.db_services = self.client.exam.services
</pre>

An example of interaction is:<br/>

<pre>
self.concert_names = {concert.get("concert_name") for concert in 
                      self.db_concerts.find(projection={"_id": 0, "concert_name": 1}) if concert.get("concert_name")}
</pre>

The query interacts with each document in the collection and returns the 
concert_name. The result is stored in a variable.

<br/>
<h2>MongoDB</h2>
<br/>

Example of one document for every collection in the MongoDB database:
<ul>
<li>concert  </li>
<p><img src = "https://github.com/Bartyxx/MongoDBConcertBooking/blob/main/img/concertDB.png"/></p>
<li>tickets  </li>
<p><img src = "https://github.com/Bartyxx/MongoDBConcertBooking/blob/main/img/ticketsDB.png"/></p>
<li>services </li>
<p><img src = "https://github.com/Bartyxx/MongoDBConcertBooking/blob/main/img/servicesDB.png"/></p>
<li>users    </li>
<p><img src = "https://github.com/Bartyxx/MongoDBConcertBooking/blob/main/img/usersDB.png"/></p>
</ul>
