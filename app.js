document.getElementById('scrapeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const url = document.getElementById('websiteUrl').value;
  
    fetch('/scrape', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url })
    })
    .then(response => response.json())
    .then(data => {
      // Update the table with the scraped data
      updateTable(data);
    })
    .catch(error => console.error('Error:', error));
  });
  
  function updateTable(data) {
    const tableBody = document.querySelector('#companyTable tbody');
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><input type="checkbox"></td>
      <td>${data.name}</td>
      <td>${data.description}</td>
      <td><img src="${data.logo}" alt="Company Logo"></td>
      <td>
        <a href="${data.facebook}" target="_blank">Facebook</a>
        <a href="${data.linkedin}" target="_blank">LinkedIn</a>
        <a href="${data.twitter}" target="_blank">Twitter</a>
        <a href="${data.instagram}" target="_blank">Instagram</a>
      </td>
      <td>
        <p>${data.address}</p>
        <p>${data.phone}</p>
        <p>${data.email}</p>
      </td>
      <td><button class="view-details" data-id="${data.id}">View Details</button></td>
    `;
    tableBody.appendChild(row);
  }
  
  // Add event listeners for delete and export functionalities
  document.getElementById('deleteSelected').addEventListener('click', function() {
    // Implement delete logic
  });
  
  document.getElementById('exportCSV').addEventListener('click', function() {
    fetch('/export', {
      method: 'GET'
    })
    .then(response => response.blob())
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = 'companies.csv';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
    })
    .catch(error => console.error('Error:', error));
  });