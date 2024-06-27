from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd
from bs4 import BeautifulSoup
import requests
import io

app = Flask(_name_)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companies.db'
db = SQLAlchemy(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    logo = db.Column(db.String(200))
    facebook = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    instagram = db.Column(db.String(200))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))

db.create_all()

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    name = soup.find('meta', {'property': 'og:site_name'})['content'] if soup.find('meta', {'property': 'og:site_name'}) else 'N/A'
    description = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else 'N/A'
    logo = soup.find('link', {'rel': 'icon'})['href'] if soup.find('link', {'rel': 'icon'}) else 'N/A'
    facebook = soup.find('a', {'href': lambda x: x and 'facebook.com' in x})['href'] if soup.find('a', {'href': lambda x: x and 'facebook.com' in x}) else 'N/A'
    linkedin = soup.find('a', {'href': lambda x: x and 'linkedin.com' in x})['href'] if soup.find('a', {'href': lambda x: x and 'linkedin.com' in x}) else 'N/A'
    twitter = soup.find('a', {'href': lambda x: x and 'twitter.com' in x})['href'] if soup.find('a', {'href': lambda x: x and 'twitter.com' in x}) else 'N/A'
    instagram = soup.find('a', {'href': lambda x: x and 'instagram.com' in x})['href'] if soup.find('a', {'href': lambda x: x and 'instagram.com' in x}) else 'N/A'
    address = soup.find('address').text if soup.find('address') else 'N/A'
    phone = soup.find('a', {'href': lambda x: x and 'tel:' in x}).text if soup.find('a', {'href': lambda x: x and 'tel:' in x}) else 'N/A'
    email = soup.find('a', {'href': lambda x: x and 'mailto:' in x}).text if soup.find('a', {'href': lambda x: x and 'mailto:' in x}) else 'N/A'

    company = Company(name=name, description=description, logo=logo, facebook=facebook, linkedin=linkedin, twitter=twitter, instagram=instagram, address=address, phone=phone, email=email)
    db.session.add(company)
    db.session.commit()

    return jsonify({'id': company.id, 'name': name, 'description': description, 'logo': logo, 'facebook': facebook, 'linkedin': linkedin, 'twitter': twitter, 'instagram': instagram, 'address': address, 'phone': phone, 'email': email})

@app.route('/export', methods=['GET'])
def export():
    companies = Company.query.all()
    data = [{
        'Name': company.name,
        'Description': company.description,
        'Logo': company.logo,
        'Facebook': company.facebook,
        'LinkedIn': company.linkedin,
        'Twitter': company.twitter,
        'Instagram': company.instagram,
        'Address': company.address,
        'Phone': company.phone,
        'Email': company.email
    } for company in companies]

    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(output, mimetype='text/csv', attachment_filename='companies.csv', as_attachment=True)

if _name_ == '_main_':
    app.run(debug=True)