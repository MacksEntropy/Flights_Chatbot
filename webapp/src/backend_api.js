import React, { useState } from 'react';

const url = "http://127.0.0.1:5000"

export default function APIRequest() {
  const [error, setError] = useState(null);

  async function fetchData() {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      setError(error);
    }
  }

  async function postData(data) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        throw new Error('Failed to post data');
      }
      const responseData = await response.json();
      return responseData;
    } catch (error) {
      setError(error);
    }
  }

  return {
    fetchData,
    postData,
    error,
  };
}

// Example usage:
// const apiUrl = 'https://api.example.com/data';
// const { fetchData, postData, error } = APIRequest({ url: apiUrl });

// // GET request example
// fetchData()
//   .then(data => {
//     console.log('GET request data:', data);
//   })
//   .catch(error => {
//     console.error('GET request error:', error);
//   });

// // POST request example
// const postData = {
//   name: 'John Doe',
//   email: 'john.doe@example.com'
// };
// postData(postData)
//   .then(response => {
//     console.log('POST request response:', response);
//   })
//   .catch(error => {
//     console.error('POST request error:', error);
//   });
