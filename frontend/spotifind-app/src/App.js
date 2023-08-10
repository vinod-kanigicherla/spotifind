import './App.css';
import AppRouter from './AppRouter';
import axios from 'axios';

axios.defaults.baseURL = 'http://0.0.0.0:8000/';

function App() {
  return (
    <>
      <AppRouter />
    </>
    );
}

export default App;
