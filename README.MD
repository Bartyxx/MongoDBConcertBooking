<!-- ---------------------------------------------------------------------- -->
<h1>MongoDBConcertBooking</h1>
<!-- ---------------------------------------------------------------------- -->

Welcome in the Python application for book concerts!<br/>
The concerts information are saved in a MongoDB database composed by 4 collection:<br/>

<ul>
<li>concert  </li>
<li>tickets  </li>
<li>services </li>
<li>users    </li>
</ul>

Python interact with MongoDB with query that returd the data askd by the users
or modify the data in the database.

<br/>
<h2>Python</h2>
<br/>

The users must register in the application to buy tickets, after insert name,
surname and tax code the users is registered. It's important to use your unique
tax code becase the primary key of the database is the tax code so if a users
insert a tax code already registered the subscription fail.<br/>

It's possible to filter by:<br/>

<ul>
<li>artist       </li>
<li>date         </li>
<li>city         </li>
<li>concert name </li>
</ul>

After choosing the concert based on the filter the users can buy the ticket.<br/>
Usually 4 position are available:<br/>
<p><img src = "https://github.com/Bartyxx/MongoDBConcertBooking/blob/main/img/sector.png"/></p>

After choosing the position and the ticket amount the total costs of the 
transaction is shown and the database is updated with the new amount of ticket
available.<br/>
<p><img src = "https://github.com/Bartyxx/MongoDBConcertBooking/blob/main/img/tickets.png"/></p>

In the end a list of services near the concert location is shown.<br/>
<p><img src = "https://github.com/Bartyxx/MongoDBConcertBooking/blob/main/img/services.png"/></p>

<br/>
<h2>Function</h2>
<br/>

Every filter is assosicated at a function that interact with the MongoDB and
return the result choosen by the users<br/>

<ul>
<li>filter_by_artist       </li>
<li>filter_by_city         </li>
<li>filter_by_concert_name </li>
<li>filter_by_date         </li>
</ul>

<br/>
<h2>Query</h2>
<br/>

Every database is initialize with a variable, those variable are used to
interact with the collection in the program<br/>

self.db_users = self.client.exam.users<br/>
self.db_tickets = self.client.exam.tickets<br/>
self.db_concerts = self.client.exam.concerts<br/>
self.db_services = self.client.exam.services<br/>

An example of interaction is:<br/>
self.concert_names = {concert.get("concert_name") for concert in 
                      self.db_concerts.find(projection={"_id": 0, "concert_name": 1}) if concert.get("concert_name")}
The query interact with every line of the collection and return the concert_name,
the result is saved in a variable.

<br/>
<h2>MongoDB</h2>
<br/>

The four collection of the MongoDB database are:
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
