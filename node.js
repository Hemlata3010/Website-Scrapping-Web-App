const express = require('express');
const cheerio = require('cheerio');
const axios = require('axios');
const { MongoClient } = require('mongodb');

const app = express();
app.use(express.json());

const dbClient = new MongoClient('mongodb://localhost:27017');
let db;

dbClient.connect().then(client => {
  db = client.db('companyData');
});

app.post('/api/scrape', async (req, res) => {
  const { url } = req.body;
  const { data } = await axios.get(url);
  const $ = cheerio.load(data);
  const companyData = {
    name: $('title').text(),
    description: $('meta[name="description"]').attr('content'),
    // Extract other data similarly
  };
  await db.collection('companies').insertOne(companyData);
  res.json(companyData);
});

app.post('/api/delete', async (req, res) => {
  const { ids } = req.body;
  await db.collection('companies').deleteMany({ _id: { $in: ids.map(id => new ObjectId(id)) } });
  res.json({ success: true });
});

app.get('/api/export', async (req, res) => {
  const companies = await db.collection('companies').find().toArray();
  let csv = 'Name,Description,Logo,Facebook,LinkedIn,Twitter,Instagram,Address,Phone,Email\n';
  companies.forEach(company => {
    csv += ${company.name},${company.description},${company.logo},${company.facebook},${company.linkedin},${company.twitter},${company.instagram},${company.address},${company.phone},${company.email}\n;
  });
  res.header('Content-Type', 'text/csv');
  res.send(csv);
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});