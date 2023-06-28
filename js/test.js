const mysql      = require('mysql');
const configdb = require('./config/db_key.json')
const connection = mysql.createConnection({
  host     : configdb.host,
  port     : configdb.port,
  user     : configdb.user,
  password : configdb.password,
  database : configdb.database
});
let express=require('express');
let app=express();
let path=require('path');
const cors=require('cors');
app.use(cors());

connection.connect();

connection.query('show databases', (error, rows, fields) => {
  if (error) throw error;
  console.log('User info is: ', rows);
});
