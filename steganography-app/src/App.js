import * as React from 'react';
import './App.css';
import Button from '@mui/material/Button';
import axios from "axios";

import logo from './logo.svg';

const baseURL = "http://localhost:8000";

function App() {
  const [post, setPost] = React.useState(null);

  React.useEffect(() => {
    axios.get(baseURL).then((response) => {
      console.log(response);
      setPost(response.data);
    });
  }, []);

  if (!post) return null;

  return (
    <div className="App">
      <Header></Header>
      <Button  variant="contained"
        onClick={() => {
          alert('clicked');
        }}>Contained</Button>
        <h1>{post.message}</h1>
        {/* <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a> */}
      
    </div>
  );
}
function Header(props){
  return(
  <div className='Header'>
    <h1 className='Text-header'>Water Marking</h1>
  </div>
  );
}

export default App;
